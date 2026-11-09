PORTNAME=	pfSense-pkg-pfBlockerNG
PORTVERSION=	3.3.14
CATEGORIES=	net
MASTER_SITES=	# empty
DISTFILES=	# empty
EXTRACT_ONLY=	# empty

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
		${PYTHON_PKGNAMEPREFIX}maxminddb>0:net/py-maxminddb@${PY_FLAVOR}

USES=		php python

CONFLICTS=	pfSense-pkg-pfBlockerNG-devel

USE_PHP=	intl
NO_BUILD=	yes
NO_MTREE=	yes

SUB_FILES=	pkg-install pkg-deinstall
SUB_LIST=	PORTNAME=${PORTNAME}

# COPYTREE_SHARE hard-links, so the payload is copied to WRKSRC first and the
# ports tree is never written to.
do-extract:
	${MKDIR} ${WRKSRC}
	(cd ${FILESDIR} && ${CP} -R etc usr ${WRKSRC})

# files/etc and files/usr are the release's src/ tree, unmodified. The
# info.xml <name> is the pfSense package-REGISTRATION name, which rc.packages
# looks up by the pfSense-pkg- PREFIX-STRIPPED name, so it is not ${PORTNAME}.
do-install:
	(cd ${WRKSRC} && ${COPYTREE_SHARE} "etc usr" ${STAGEDIR})
	@${REINPLACE_CMD} -i '' \
		-e 's|%%PKGNAME%%|${PORTNAME:S/pfSense-pkg-//}|' \
		-e 's|%%PKGVERSION%%|${PKGVERSION}|' \
		${STAGEDIR}${DATADIR}/info.xml
	${CHMOD} ${BINMODE} \
		${STAGEDIR}${PREFIX}/etc/rc.d/pfblockerng_repo_generate.sh \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng/*.sh \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng/*.py \
		${STAGEDIR}${PREFIX}/pkg/pfblockerng/pfb_unbound_include.inc \
		${STAGEDIR}${PREFIX}/www/pfblockerng/www/*.php

.include <bsd.port.mk>
