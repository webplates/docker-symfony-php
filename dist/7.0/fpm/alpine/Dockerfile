FROM php:7.0.9-fpm-alpine

ENV COMPOSER_VERSION=1.1.0 COMPOSER_ALLOW_SUPERUSER=1
ENV SYMFONY_ENV prod

WORKDIR /app

RUN set -xe \
    && apk add --no-cache git coreutils freetype-dev libjpeg-turbo-dev libltdl libmcrypt-dev libpng-dev icu icu-libs icu-dev unzip \
    && docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ \
    && docker-php-ext-install -j$(nproc) iconv mbstring mcrypt intl pdo_mysql gd zip \
    && echo "[PHP]\n\ndate.timezone = UTC" > /usr/local/etc/php/php.ini \
    && curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer --version=${COMPOSER_VERSION} \
    && composer global require --quiet "hirak/prestissimo:^0.3" \
    && rm -rf /usr/local/etc/php/php.ini
