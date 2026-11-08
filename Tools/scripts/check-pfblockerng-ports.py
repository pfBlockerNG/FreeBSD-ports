#!/usr/bin/env python3
"""Check both release payloads in real packages.

Pass --stable-pkg and --devel-pkg for native `make package` outputs.
--stable-src and --devel-src point at the extracted, pinned release trees.
Native checksums require `pkg checksum` on PATH; run native checks on FreeBSD.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import runpy
import tarfile
import tempfile
import xml.etree.ElementTree as ET


def check(source, suffix, version, package_path):
    portname = "pfSense-pkg-pfBlockerNG" + suffix
    with tempfile.TemporaryDirectory(prefix="pfb-port-check-") as temporary:
        out = Path(temporary)
        with tarfile.open(package_path) as archive:
            members = {m.name.lstrip("./"): m for m in archive.getmembers() if m.isfile()}

            def read(path):
                stream = archive.extractfile(members[path.lstrip("/")])
                assert stream is not None, f"{portname}: missing {path}"
                return stream.read()

            manifest = json.loads(read("+MANIFEST"))
            expected_files = set()
            executable_patterns = (
                "usr/local/etc/rc.d/pfblockerng_repo_generate.sh",
                "usr/local/pkg/pfblockerng/*.sh",
                "usr/local/pkg/pfblockerng/*.py",
                "usr/local/pkg/pfblockerng/pfb_unbound_include.inc",
                "usr/local/www/pfblockerng/www/*.php",
            )
            if suffix:
                executable_patterns += (
                    "usr/local/pkg/pfblockerng/list_scripts/*.sh",
                    "usr/local/pkg/pfblockerng/dns_proxy/pfb_dns.sh",
                )
            for file in (source / "src").rglob("*"):
                if not file.is_file():
                    continue
                relative = file.relative_to(source / "src").as_posix()
                expected = file.read_bytes()
                if relative == "usr/local/share/pfSense-pkg-pfBlockerNG/info.xml":
                    relative = "usr/local/share/" + portname + "/info.xml"
                    expected = expected.replace(b"%%PKGNAME%%", ("pfBlockerNG" + suffix).encode())
                    expected = expected.replace(b"%%PKGVERSION%%", version.encode())
                elif suffix and relative == "usr/local/pkg/pfblockerng/pfb_python.sh":
                    expected = expected.replace(b"%%PYTHON_SUFFIX%%", b"311")
                expected_files.add(relative)
                assert read(relative) == expected, f"{portname}: {relative} differs from release src/"
                if file.stat().st_mode & 0o111 or any(Path(relative).match(p) for p in executable_patterns):
                    assert members[relative].mode & 0o111 == 0o111, f"{relative} lost executable bits"
            assert manifest["name"] == portname and manifest["version"] == version, "package identity"
            package = ET.fromstring(read("usr/local/share/" + portname + "/info.xml")).find("package")
            assert package is not None, "registration package element missing"
            assert package.findtext("name") == "pfBlockerNG" + suffix, "registration name"
            assert package.findtext("version") == version, "installed version"
            payload = {"/" + name for name in members if not name.startswith("+")}
            assert set(manifest["files"]) == payload, "manifest/plist coverage differs from payload"
            for path, entry in manifest["files"].items():
                if entry["sum"].startswith("1$"):
                    assert entry["sum"] == "1$" + hashlib.sha256(read(path)).hexdigest(), path
                else:
                    payload_file = out / "checksum"
                    payload_file.write_bytes(read(path))
                    subprocess.run(["pkg", "checksum", "-q", "-c", entry["sum"], str(payload_file)], check=True)
            assert set(manifest["scripts"]) == {"install", "deinstall"}, "lifecycle scripts missing"
            licenses = ("APACHE20", "BSD3CLAUSE", "MIT") if suffix else ("APACHE20",)
            expected_files.update(
                f"usr/local/share/licenses/{portname}-{version}/{name}"
                for name in (*licenses, "LICENSE", "catalog.mk")
            )
            if suffix:
                helper = runpy.run_path(str(source / "scripts" / "build-pfb-dns.py"))
                for arch, machine in (("amd64", 62), ("arm64", 183)):
                    binary = "usr/local/pkg/pfblockerng/dns_proxy/bin/freebsd-" + arch + "/pfb-dns"
                    expected_files.add(binary)
                    helper["_check_elf"](
                        Path(binary), read(binary), "freebsd-" + arch, machine,
                        int(manifest["abi"].split(":")[1]),
                    )
                    assert members[binary].mode & 0o111 == 0o111, f"{binary} not executable"
            assert payload == {"/" + name for name in expected_files}, "package differs from release inventory"
            print(f"PASS {portname} {version}: {len(payload)} packaged files")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stable-pkg", type=Path, required=True)
    parser.add_argument("--devel-pkg", type=Path, required=True)
    parser.add_argument("--stable-src", type=Path, required=True)
    parser.add_argument("--devel-src", type=Path, required=True)
    args = parser.parse_args()
    check(args.stable_src.resolve(), "", "3.3.14", args.stable_pkg)
    check(args.devel_src.resolve(), "-devel", "4.0.0.b1", args.devel_pkg)


if __name__ == "__main__":
    main()
