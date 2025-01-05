import hashlib
import ssl
from cryptography import x509
from cryptography.hazmat.primitives import serialization

def get_cert_hash(cert_pem):
    """Funkcja do obliczania hasza certyfikatu"""
    # Ładowanie certyfikatu X.509 z formatu PEM
    cert = x509.load_pem_x509_certificate(cert_pem.encode('utf-8'))

    # Serializacja certyfikatu do formatu DER
    cert_der = cert.public_bytes(serialization.Encoding.DER)

    # Obliczanie hasza certyfikatu w formacie SHA-256
    cert_hash = hashlib.sha256(cert_der).hexdigest().upper()

    return cert_hash

# Przykład użycia
cert_pem = """-----BEGIN CERTIFICATE-----
MIID7zCCAtegAwIBAgIUIBCJF1IJYaIpcWNj6ftVjlIVc5owDQYJKoZIhvcNAQEL
BQAwgYYxCzAJBgNVBAYTAlBMMQ8wDQYDVQQIDAZLaWVsY2UxDzANBgNVBAcMBktp
ZWxjZTEMMAoGA1UECgwDUFNLMQwwCgYDVQQLDANQU0sxDDAKBgNVBAMMA1BTSzEr
MCkGCSqGSIb3DQEJARYcczA5MTI4OUBzdHVkZW50LnR1LmtpZWxjZS5wbDAeFw0y
NTAxMDQyMTQ0MzFaFw0yNjAxMDQyMTQ0MzFaMIGGMQswCQYDVQQGEwJQTDEPMA0G
A1UECAwGS2llbGNlMQ8wDQYDVQQHDAZLaWVsY2UxDDAKBgNVBAoMA1BTSzEMMAoG
A1UECwwDUFNLMQwwCgYDVQQDDANQU0sxKzApBgkqhkiG9w0BCQEWHHMwOTEyODlA
c3R1ZGVudC50dS5raWVsY2UucGwwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEK
AoIBAQDKSjccjYv9hjQ6x9a1Drv362aikL7qV3Hs64nu/GWxbd5DaOcUqrNy3RyD
pDVfChG4Anm3BNzayd1WnSClMhoIEfONCV4SC3rq+2Zh8fWmWuj050+TugUqnzzi
7B0m2qxPzkJowwHuaX7v5kfa7VtU3o7HP1fMU4rczpx3v3zhOL1vkwGp8mwnZZ+A
IBxAaL1KiQRBZOD2iWQIsGploq/lperMmgkFcueIcE/zgySLdcfYadhpWtP4WPfJ
plYr/krdsDKD1nkeYjXyHf0vF63qbz4CpQ4R71xj8ZA3Wdz/OpmE0vSNERaAeKs0
QHXItCll/Sym9yIQ8OXTH5V8k0K3AgMBAAGjUzBRMB0GA1UdDgQWBBS3FsnyLQzn
+U4uqpwKY5wUDECckzAfBgNVHSMEGDAWgBS3FsnyLQzn+U4uqpwKY5wUDECckzAP
BgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3DQEBCwUAA4IBAQAzf99U/zOTcimcmvvz
RVSBuq7tVTzqbVbYXMVOPWxQR+9Da/fHGJk3dt6y2TVCORrMlQ1Tah3wvm9jecZs
Gb+s2oO/eEqd8tfdJwNvagQQTGkBv6FHamEfGdQxcvwd9h6NfADsQYgKOjv8SiaK
2vvXJF43VOo9L/2dOhmGHlF5s9WH09E8UJgPRLn44du5cmdd+y8qGaHPElBOFsEZ
73Qz170l7bt6eMzHoS+oBBtY1eWm+dK+kEQP2byYx0pTxz/KvhLDe1rYhXS9kBNW
cJ7Vjrrf4Qn47VlmPBuu2iHW1hI/eAbPohzbgHXALzLkjfK2S+jtGM2ejHygYzg3
AHil
-----END CERTIFICATE-----
"""

cert_hash = get_cert_hash(cert_pem)
print(cert_hash)
