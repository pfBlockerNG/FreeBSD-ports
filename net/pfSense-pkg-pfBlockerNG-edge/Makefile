PORTNAME=	pfSense-pkg-pfBlockerNG-edge
PORTVERSION=	4.0.0.a1
CATEGORIES=	net

MAINTAINER=	coreteam@pfsense.org
COMMENT=	pfSense package pfBlockerNG

LICENSE=	APACHE20

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

USES=		php python

NO_ARCH=	yes

CONFLICTS=	pfSense-pkg-pfBlockerNG pfSense-pkg-pfBlockerNG-testing pfSense-pkg-pfBlockerNG-nightly

USE_PHP=	intl
NO_BUILD=	yes
NO_MTREE=	yes

USE_GITHUB=	yes
GH_ACCOUNT=	pfBlockerNG
GH_PROJECT=	pfBlockerNG
GH_TAGNAME=	v${PORTVERSION}
DIST_SUBDIR=	${PORTNAME}

# GitHub extracts to <project>-<version>/; production files live under src/
WRKSRC=		${WRKDIR}/${GH_PROJECT}-${PORTVERSION}/src

TEST_DEPENDS=	${PYTHON_PKGNAMEPREFIX}pytest>=0:devel/py-pytest@${PY_FLAVOR}

SUB_FILES=	pkg-install pkg-deinstall
SUB_LIST=	PORTNAME=${PORTNAME}
PLIST_DIRS=	/var/unbound /etc/inc/priv /etc/inc

# The info.xml <name> is the pfSense package-REGISTRATION name, which rc.packages
# (install_package_xml -> get_package_id) looks up by the pfSense-pkg- PREFIX-STRIPPED
# name. So it MUST be the short name (pfBlockerNG-edge), NOT the full ${PORTNAME}.
post-extract:
	@${SED} -i '' 's|%%PKGNAME%%|${PORTNAME:S/pfSense-pkg-//}|g' \
		${WRKSRC}/usr/local/share/pfSense-pkg-pfBlockerNG/info.xml
	@${REINPLACE_CMD} -e 's|%%PYTHON_SUFFIX%%|${PYTHON_SUFFIX}|g' \
		${WRKSRC}/usr/local/pkg/pfblockerng/pfb_python.sh
	@mv ${WRKSRC}/usr/local/share/pfSense-pkg-pfBlockerNG \
		${WRKSRC}/usr/local/share/${PORTNAME}

do-install:
	(cd ${WRKSRC} && ${COPYTREE_SHARE} . ${STAGEDIR})
	${MKDIR} ${STAGEDIR}/etc/inc/priv
	${MKDIR} ${STAGEDIR}${PREFIX}/pkg/firewall_aliases_edit/pre_write_config
	${MKDIR} ${STAGEDIR}${PREFIX}/pkg/pfblockerng
	${MKDIR} ${STAGEDIR}${PREFIX}/pkg/pfblockerng/list_scripts
	${MKDIR} ${STAGEDIR}${PREFIX}/www/pfblockerng/www
	${MKDIR} ${STAGEDIR}${PREFIX}/www/widgets/widgets
	${MKDIR} ${STAGEDIR}${PREFIX}/www/widgets/include
	${MKDIR} ${STAGEDIR}${PREFIX}/www/widgets/javascript
	${MKDIR} ${STAGEDIR}${PREFIX}/www/wizards
	${MKDIR} ${STAGEDIR}${PREFIX}/www/shortcuts
	${MKDIR} ${STAGEDIR}/var/unbound
	${MKDIR} ${STAGEDIR}${DATADIR}
	${INSTALL_SCRIPT} ${WRKSRC}${PREFIX}/etc/rc.d/pfblockerng_repo_generate.sh \
		${STAGEDIR}${PREFIX}/etc/rc.d
	${INSTALL_SCRIPT} ${WRKSRC}${PREFIX}/pkg/pfblockerng/*.sh \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng
	${INSTALL_SCRIPT} ${WRKSRC}${PREFIX}/pkg/pfblockerng/*.py \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng
	${INSTALL_SCRIPT} ${WRKSRC}${PREFIX}/pkg/pfblockerng/list_scripts/*.sh \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng/list_scripts
	${INSTALL_SCRIPT} ${WRKSRC}${PREFIX}/pkg/pfblockerng/pfb_unbound_include.inc \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng
	${INSTALL_SCRIPT} ${WRKSRC}${PREFIX}/www/pfblockerng/www/*.php \
		${STAGEDIR}${PREFIX}/www/pfblockerng/www
	${INSTALL_DATA} -m 0644 ${WRKSRC}${PREFIX}/pkg/pfblockerng.xml \
		${STAGEDIR}${PREFIX}/pkg
	${INSTALL_DATA} ${WRKSRC}/etc/inc/priv/pfblockerng.priv.inc \
		${STAGEDIR}/etc/inc/priv
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/pkg/pfblockerng/pfblockerng.inc \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/pkg/pfblockerng/pfblockerng_apply.inc \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/pkg/pfblockerng/pfblockerng_cron.inc \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/pkg/pfblockerng/pfblockerng_geoip.inc \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/pkg/pfblockerng/pfblockerng_install.inc \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/pkg/pfblockerng/pfblockerng_extra.inc \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/pkg/firewall_aliases_edit/pre_write_config/pfblockerng.php \
		${STAGEDIR}${PREFIX}/pkg/firewall_aliases_edit/pre_write_config
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/www/pfblockerng/pfBlockerNG.js \
		${STAGEDIR}${PREFIX}/www/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/www/pfblockerng/pfblockerng_asn.txt \
		${STAGEDIR}${PREFIX}/www/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/www/shortcuts/pkg_pfblockerng.inc \
		${STAGEDIR}${PREFIX}/www/shortcuts
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/www/pfblockerng/pfblockerng.php \
		${STAGEDIR}${PREFIX}/www/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/www/pfblockerng/pfblockerng_alerts.php \
		${STAGEDIR}${PREFIX}/www/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/www/pfblockerng/pfblockerng_blacklist.php \
		${STAGEDIR}${PREFIX}/www/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/www/pfblockerng/pfblockerng_category.php \
		${STAGEDIR}${PREFIX}/www/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/www/pfblockerng/pfblockerng_category_edit.php \
		${STAGEDIR}${PREFIX}/www/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/www/pfblockerng/pfblockerng_dnsbl.php \
		${STAGEDIR}${PREFIX}/www/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/www/pfblockerng/pfblockerng_feeds.json \
		${STAGEDIR}${PREFIX}/www/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/www/pfblockerng/pfblockerng_feeds.php \
		${STAGEDIR}${PREFIX}/www/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/www/pfblockerng/pfblockerng_general.php \
		${STAGEDIR}${PREFIX}/www/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/www/pfblockerng/pfblockerng_hooks.php \
		${STAGEDIR}${PREFIX}/www/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/www/pfblockerng/pfblockerng_ip.php \
		${STAGEDIR}${PREFIX}/www/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/www/pfblockerng/pfblockerng_update.php \
		${STAGEDIR}${PREFIX}/www/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/www/pfblockerng/pfblockerng_sync.php \
		${STAGEDIR}${PREFIX}/www/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/www/pfblockerng/pfblockerng_safesearch.php \
		${STAGEDIR}${PREFIX}/www/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/www/pfblockerng/pfblockerng_software.php \
		${STAGEDIR}${PREFIX}/www/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/www/pfblockerng/pfblockerng_threats.php \
		${STAGEDIR}${PREFIX}/www/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/www/pfblockerng/pfblockerng_log.php \
		${STAGEDIR}${PREFIX}/www/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/www/widgets/widgets/pfblockerng.widget.php \
		${STAGEDIR}${PREFIX}/www/widgets/widgets
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/www/widgets/include/widget-pfblockerng.inc \
		${STAGEDIR}${PREFIX}/www/widgets/include
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/www/widgets/javascript/pfblockerng.js \
		${STAGEDIR}${PREFIX}/www/widgets/javascript
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/www/wizards/pfblockerng_wizard.xml \
		${STAGEDIR}${PREFIX}/www/wizards/pfblockerng_wizard.xml
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/www/wizards/pfblockerng_wizard.inc \
		${STAGEDIR}${PREFIX}/www/wizards/pfblockerng_wizard.inc
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/pkg/pfblockerng/dnsbl_* \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/pkg/pfblockerng/shallalist_global_usage \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/pkg/pfblockerng/ut1_global_usage \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/pkg/pfblockerng/pfb_dnsbl.doh.conf \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/pkg/pfblockerng/pfb_dnsbl.safesearch.conf \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/pkg/pfblockerng/pfb_dnsbl.youtube_restrict.conf \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/pkg/pfblockerng/pfb_dnsbl.youtube_restrictmoderate.conf \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${PREFIX}/pkg/pfblockerng/pfb_py_hsts.txt \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng
	${INSTALL_DATA} ${WRKSRC}${DATADIR}/info.xml \
		${STAGEDIR}${DATADIR}
	@${REINPLACE_CMD} -i '' -e "s|%%PKGVERSION%%|${PKGVERSION}|" \
		${STAGEDIR}${DATADIR}/info.xml

post-install:
	@${FIND} -s ${STAGEDIR}${PREFIX} -type f -print | \
		${SED} -e "s#${STAGEDIR}${PREFIX}/##g" >> ${TMPPLIST}
	@${FIND} -s ${STAGEDIR}/etc -type f -print | \
		${SED} -e "s#${STAGEDIR}##g" >> ${TMPPLIST}

do-test:
	cd ${WRKSRC:H} && \
		${SETENV} ${TEST_ENV} ${PYTHON_CMD} -m pytest -v

.include <bsd.port.mk>
