# wis2box-minio

This is a fork of the MinIO source-code that is archived at github.com/minio/minio. The source code is used to build a MinIO image for the WIS2BOX project. 

Note that wis2box is not affiliated with MinIO, and this repository is maintained independently for the purpose of building a custom MinIO image for the WIS2BOX project. The WIS2BOX project is a non-commercial initiative, aimed to provide a low-barrier, open-source solution to help accelerate WIS2 implementations in support of GBON and the WMO unified data policy.

This fork is originally based of the tag=RELEASE.2024-08-03T04-33-23Z, which was the version of minio include in wis2box-1.2.0. 

wis2box-minio uses GNU Affero General Public License to match the license of the original MinIO source code. If you want to use this code, please make sure to comply with the terms of the license.

The image can be built locally with the following command:

```
docker build -t wis2box-minio:latest -f Dockerfile.local --build-arg RELEASE=local-build-test.
```

## development

You can use the docker-compose.yml to start a development environment:

```
docker compose -f docker-compose.yml up -d
```

You can access the dev container with:

```
docker compose exec go-dev sh 
```

You can use the following command to run go mod tidy in the dev container to update the go.mod and go.sum files after making changes to the code:

```
docker compose exec go-dev go mod tidy
```
