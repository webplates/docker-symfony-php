FROM php:7.0.11-fpm

ENV COMPOSER_VERSION=1.1.0 COMPOSER_ALLOW_SUPERUSER=1 COMPOSER_PATH=/usr/local/bin
ENV SYMFONY_ENV prod

WORKDIR /app

RUN set -xe \
    && apt-get update \
    && apt-get install -qqy git libfreetype6-dev libjpeg62-turbo-dev libmcrypt-dev libpng12-dev libicu-dev unzip \
    && chown -R www-data. /var/www \
    && docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ \
    && docker-php-ext-install -j$(nproc) iconv mbstring mcrypt intl pdo_mysql gd zip \
    && curl -sS https://getcomposer.org/installer | php -- --install-dir=${COMPOSER_PATH} --filename=composer --version=${COMPOSER_VERSION} \
    && export COMPOSER_COMMAND="composer" \
    && $COMPOSER_COMMAND global require --quiet "hirak/prestissimo:^0.3"
