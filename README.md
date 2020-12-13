# Mender Mongo DB linter

The `mender_lint_db` tool performs linting and maintenance in an Enterprise Mender
installation.

## Troubleshooting

If the Python script fails with TLS-related issues, run the following command:

```bash
$ export SSL_CERT_FILE=$(python -c "import certifi; print(certifi.where())")
```
