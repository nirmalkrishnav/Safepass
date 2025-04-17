# Secret Share API

A SaaS application that securely stores and shares secrets using AES encryption. Users submit a title and plaintext secret, which is encrypted and stored. The system returns a unique ID for each secret, which can later be used to retrieve and decrypt the secret.

Secrets are stored with encryption keys and initialization vectors (IVs), but only the ID is returned to the user. The user can use the ID to retrieve the secret, with the decryption process handled on the server side.
