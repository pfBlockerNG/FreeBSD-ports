PORTNAME=	pfSense-pkg-pfBlockerNG-devel
PORTVERSION=	4.0.0.b1
CATEGORIES=	net
MASTER_SITES=	# empty
DISTFILES=	# empty
EXTRACT_ONLY=	# empty

MAINTAINER=	coreteam@pfsense.org
COMMENT=	pfSense package pfBlockerNG

# pfBlockerNG is Apache-2.0. pfb-dns also compiles in the Go runtime and
# golang.org/x/{crypto,net,sys} (BSD-3-Clause), quic-go (MIT) and
# go-proxyproto (Apache-2.0); the licence texts are the vendored ones.
LICENSE=	APACHE20 BSD3CLAUSE MIT
LICENSE_COMB=	multi
LICENSE_FILE_APACHE20=	${FILESDIR}/go/pfb_dns_gateway/vendor/github.com/pires/go-proxyproto/LICENSE
LICENSE_FILE_BSD3CLAUSE=	${FILESDIR}/go/pfb_dns_gateway/vendor/golang.org/x/net/LICENSE
LICENSE_FILE_MIT=	${FILESDIR}/go/pfb_dns_gateway/vendor/github.com/quic-go/quic-go/LICENSE

RUN_DEPENDS=	${LOCALBASE}/bin/mmdblookup:net/libmaxminddb \
		${LOCALBASE}/bin/ggrep:textproc/gnugrep \
		${LOCALBASE}/bin/grepcidr:net-mgmt/grepcidr \
		${LOCALBASE}/bin/iprange:net-mgmt/iprange \
		${LOCALBASE}/bin/jq:textproc/jq \
		${LOCALBASE}/bin/rsync:net/rsync \
		${LOCALBASE}/sbin/lighttpd:www/lighttpd \
		${PYTHON_PKGNAMEPREFIX}sqlite3>0:databases/py-sqlite3@${PY_FLAVOR} \
		${PYTHON_PKGNAMEPREFIX}maxminddb>0:net/py-maxminddb@${PY_FLAVOR} \
		${PYTHON_PKGNAMEPREFIX}charset-normalizer>0:textproc/py-charset-normalizer@${PY_FLAVOR}

USES=		go:1.26+,modules,no_targets php python

NO_ARCH=	yes
# One static FreeBSD pfb-dns per architecture; dns_proxy/pfb_dns.sh picks this machine's at run time.
NO_ARCH_IGNORE=	pfb-dns

CONFLICTS=	pfSense-pkg-pfBlockerNG

USE_PHP=	intl
NO_MTREE=	yes
# Ship the bytes do-build checked (go already strips with -ldflags "-s -w").
STRIP=

SUB_FILES=	pkg-install pkg-deinstall
SUB_LIST=	PORTNAME=${PORTNAME}

# COPYTREE_SHARE hard-links, so the payload is copied to WRKSRC first and the
# ports tree is never written to.
do-extract:
	${MKDIR} ${WRKSRC}
	(cd ${FILESDIR} && ${CP} -R etc usr ${WRKSRC})

# files/go and files/scripts are the release's go/pfb_dns_gateway (with its
# modules vendored by `go mod vendor`) and scripts/build-pfb-dns.py: build-only.
do-build:
	(cd ${WRKDIR} && ${SETENVI} ${WRK_ENV} ${GO_ENV} ${PYTHON_CMD} ${FILESDIR}/scripts/build-pfb-dns.py \
		--source-root ${FILESDIR} --out-dir ${WRKDIR}/pfb-dns --go ${GO_CMD} --vendored \
		--freebsd-major ${OSREL:R})

# files/etc and files/usr are the release's src/ tree, unmodified. The
# info.xml <name> is the pfSense package-REGISTRATION name, which rc.packages
# looks up by the pfSense-pkg- PREFIX-STRIPPED name, so it is not ${PORTNAME};
# the release names the share directory pfSense-pkg-pfBlockerNG.
do-install:
	(cd ${WRKSRC} && ${COPYTREE_SHARE} "etc usr" ${STAGEDIR})
	${MV} ${STAGEDIR}${PREFIX}/share/pfSense-pkg-pfBlockerNG ${STAGEDIR}${DATADIR}
	@${REINPLACE_CMD} -i '' \
		-e 's|%%PKGNAME%%|${PORTNAME:S/pfSense-pkg-//}|' \
		-e 's|%%PKGVERSION%%|${PKGVERSION}|' \
		${STAGEDIR}${DATADIR}/info.xml
	@${REINPLACE_CMD} -i '' -e 's|%%PYTHON_SUFFIX%%|${PYTHON_SUFFIX}|g' \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng/pfb_python.sh
	${MKDIR} ${STAGEDIR}${PREFIX}/pkg/pfblockerng/dns_proxy/bin/freebsd-amd64 \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng/dns_proxy/bin/freebsd-arm64
	${INSTALL_PROGRAM} ${WRKDIR}/pfb-dns/freebsd-amd64/pfb-dns \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng/dns_proxy/bin/freebsd-amd64
	${INSTALL_PROGRAM} ${WRKDIR}/pfb-dns/freebsd-arm64/pfb-dns \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng/dns_proxy/bin/freebsd-arm64
	${CHMOD} ${BINMODE} \
		${STAGEDIR}${PREFIX}/etc/rc.d/pfblockerng_repo_generate.sh \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng/*.sh \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng/*.py \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng/pfb_unbound_include.inc \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng/dns_proxy/pfb_dns.sh \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng/list_scripts/*.sh \
		${STAGEDIR}${PREFIX}/www/pfblockerng/www/*.php

.include <bsd.port.mk>
