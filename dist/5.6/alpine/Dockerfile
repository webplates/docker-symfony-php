FROM php:5.6.25-alpine

ENV COMPOSER_VERSION=1.1.0 COMPOSER_ALLOW_SUPERUSER=1 COMPOSER_PATH=/usr/local/bin
ENV SYMFONY_ENV prod

WORKDIR /app

RUN set -xe \
    && apk add --no-cache git coreutils freetype-dev libjpeg-turbo-dev libltdl libmcrypt-dev libpng-dev icu icu-libs icu-dev unzip \
    && docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ \
    && docker-php-ext-install -j$(nproc) iconv mbstring mcrypt intl pdo_mysql gd zip \
    && curl -sS https://getcomposer.org/installer | php -- --install-dir=${COMPOSER_PATH} --filename=composer --version=${COMPOSER_VERSION} \
    && export COMPOSER_COMMAND="php -d date.timezone=UTC ${COMPOSER_PATH}/composer" \
    && $COMPOSER_COMMAND global require --quiet "hirak/prestissimo:^0.3"
