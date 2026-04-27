
FROM golang:1.25-alpine as build

ARG TARGETARCH
ARG RELEASE

ENV GOPATH /go
ENV CGO_ENABLED 0
WORKDIR /src

# Install build dependencies
RUN apk add -U --no-cache ca-certificates git

# Download static Linux curl binary
ADD https://github.com/moparisthebest/static-curl/releases/download/v8.17.0/curl-amd64 /usr/bin/curl
RUN chmod +x /usr/bin/curl

# Copy go mod and sum files first for better caching and dependency management
COPY go.mod go.sum ./
RUN go mod download

# Copy the rest of the source code
COPY . .

# Build minio binary with version info
RUN go build -ldflags "$(go run buildscripts/gen-ldflags.go)" -o /go/bin/minio ./

# Optionally build mc if source is present (remove if not needed)
# RUN git clone https://github.com/minio/mc.git /src-mc && cd /src-mc && go build -o /go/bin/mc ./

FROM registry.access.redhat.com/ubi9/ubi-micro:latest

ARG RELEASE

LABEL name="wis2box-minio" \
      maintainer="Maaike Limper <maaike.limper@gmail.com>" \
      version="${RELEASE}" \
      release="${RELEASE}" \
      summary="MinIO storage providing S3-compatible object storage for the WIS2BOX project." \
      description="MinIO storage providing S3-compatible object storage for the WIS2BOX project."

ENV MINIO_ACCESS_KEY_FILE=access_key \
    MINIO_SECRET_KEY_FILE=secret_key \
    MINIO_ROOT_USER_FILE=access_key \
    MINIO_ROOT_PASSWORD_FILE=secret_key \
    MINIO_KMS_SECRET_KEY_FILE=kms_master_key \
    MINIO_CONFIG_ENV_FILE=config.env \
    MC_CONFIG_DIR=/tmp/.mc

COPY --from=build /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=build /go/bin/minio /usr/bin/minio
# Copy static curl binary from build stage
COPY --from=build /usr/bin/curl /usr/bin/curl
#COPY --from=build /go/bin/mc /usr/bin/mc
COPY CREDITS /licenses/CREDITS
COPY LICENSE /licenses/LICENSE

COPY dockerscripts/docker-entrypoint.sh /usr/bin/docker-entrypoint.sh
RUN chmod +x /usr/bin/docker-entrypoint.sh

EXPOSE 9000
VOLUME ["/data"]

ENTRYPOINT ["/usr/bin/docker-entrypoint.sh"]
CMD ["minio"]
