ROOT_MKFILE := ${realpath ${dir ${firstword ${MAKEFILE_LIST}}}}
PREFIX := ${ROOT_MKFILE}/make-build
CACHE := ${ROOT_MKFILE}/make-cache

LIB := ${PREFIX}/lib
LIB64 := ${PREFIX}/lib64
BIN := ${PREFIX}/bin
INCLUDE := ${PREFIX}/include

# Other curl deps that was pulled that ain't here yet
# nghttp2 idn2 rtmp psl ldap lber zstd brotlidec zlib

LIBS := ${LIB}/libdiscord.a \
		${LIB}/libcurl.a \
		${LIB}/libffmpegthumbnailer.a \
		${LIB}/libjson-c.a \
		${LIB}/libopus.a \
		${LIB64}/libssl.a \
		${LIB}/libx264.a

all: ${LIBS}

${LIB}/libdiscord.a: ${LIB}/libcurl.a
	${MAKE} -C 3rd_party/concord PREFIX=${PREFIX} clean
	${MAKE} -C 3rd_party/concord PREFIX=${PREFIX} shared
	${MAKE} -C 3rd_party/concord PREFIX=${PREFIX} install
	${MAKE} -C 3rd_party/concord PREFIX=${PREFIX} clean
	${MAKE} -C 3rd_party/concord PREFIX=${PREFIX} static
	${MAKE} -C 3rd_party/concord PREFIX=${PREFIX} install

${LIB}/libcurl.a: ${LIB64}/libssl.a
	cd 3rd_party/curl; autoreconf -fi
	cd 3rd_party/curl; ./configure \
		--prefix=${PREFIX} \
		--with-openssl \
		--enable-shared
	${MAKE} -C 3rd_party/curl clean
	${MAKE} -C 3rd_party/curl install
	cd 3rd_party/curl; ./configure \
		--prefix=${PREFIX} \
		--with-openssl \
		--enable-static
	${MAKE} -C 3rd_party/curl clean
	${MAKE} -C 3rd_party/curl install

${LIB}/libffmpegthumbnailer.a: ${LIB}/libopus.a ${LIB}/libx264.a
	cd 3rd_party/ffmpeg; ./configure \
		--prefix=${PREFIX} \
		--enable-shared \
		--disable-asm
	${MAKE} -C 3rd_party/ffmpeg clean
	${MAKE} -C 3rd_party/ffmpeg install
	cd 3rd_party/ffmpeg; ./configure \
		--prefix=${PREFIX} \
		--enable-static \
		--disable-asm
	${MAKE} -C 3rd_party/ffmpeg clean
	${MAKE} -C 3rd_party/ffmpeg install

${LIB}/libjson-c.a:
	cmake -B ${CACHE}/cmake/json-c \
		-DCMAKE_PREFIX_PATH=${PREFIX} \
		-DCMAKE_INSTALL_PREFIX=${PREFIX} \
		-DCMAKE_BUILD_TYPE=release \
		-DBUILD_SHARED_LIBS="ON" \
		-DBUILD_STATIC_LIBS="ON" \
		3rd_party/json-c
	${MAKE} -C ${CACHE}/cmake/json-c clean
	${MAKE} -C ${CACHE}/cmake/json-c install

${LIB}/libopus.a:
	cd 3rd_party/opus; ./autogen.sh
	cd 3rd_party/opus; ./configure \
		--prefix=${PREFIX} \
		--enable-shared
	${MAKE} -C 3rd_party/opus clean
	${MAKE} -C 3rd_party/opus install
	cd 3rd_party/opus; ./configure \
		--prefix=${PREFIX} \
		--enable-static
	${MAKE} -C 3rd_party/opus clean
	${MAKE} -C 3rd_party/opus install

${LIB64}/libssl.a:
	# Can't make this go parallel or else it would fail saying 
	# apps/CA.pl can't be statted
	cd 3rd_party/openssl; ./Configure \
		--prefix=${PREFIX}
	${MAKE} -C 3rd_party/openssl clean
	${MAKE} -C 3rd_party/openssl -j1 install
	cd 3rd_party/openssl; ./Configure \
		--prefix=${PREFIX} \
		-static
	${MAKE} -C 3rd_party/openssl clean
	${MAKE} -C 3rd_party/openssl -j1 install

${LIB}/libx264.a:
	cd 3rd_party/x264; ./configure \
		--prefix=${PREFIX} \
		--enable-shared \
		--disable-asm
	${MAKE} -C 3rd_party/x264 clean
	${MAKE} -C 3rd_party/x264 install
	cd 3rd_party/x264; ./configure \
		--prefix=${PREFIX} \
		--enable-static \
		--disable-asm
	${MAKE} -C 3rd_party/x264 clean
	${MAKE} -C 3rd_party/x264 install
