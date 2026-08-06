# Provenans, Kanıt Desteği ve Güvenli Sentez

## Kesin ayrım

| Terim | Ne gösterir? | Otomatik üretilebilir mi? |
|---|---|---:|
| `LEXICAL_SUPPORT` | Claim ile bir bank girdisi arasında sözcüksel örtüşme | Evet |
| `UNVERIFIED` | Kaynak olgusal olarak incelenmedi | Evet |
| `VERIFIED` | Kaynak locator/hash üzerinden olgusal inceleme tamamlandı | Hayır; kaynak/insan incelemesi gerekir |
| `PASS` | İlgili gate’in tüm sözleşmesi karşılandı | Yalnız kanıtla |

`evidence_bank.provenance_check()` artık lexical eşleşmeyi “doğrulandı” veya `PASS`
olarak adlandırmaz. Tüm eşleşmeler `UNVERIFIED/REVIEW` başlar.

## v2 kaynak zinciri

`SourceArtifact → CandidateFact → EvidenceRecord → RequirementEvidenceMap → SynthesisChangeSet`

Her kaynak artifact filename, media type, SHA-256, locator ve version taşır. Her sentez
değişikliği bilinen evidence ID ister. `safe_synthesis.py` yalnız `cv.summary`,
`cv.experience`, `cv.skills`, `cv.education`, `cv.certifications` yollarında öneri kabul eder.

Şirket, unvan, başlangıç/bitiş tarihi, derece, dil seviyesi ve metrik alanları korumalıdır.
İnsan onayı olmadan change set `REVIEW` durumundadır.

## Tehdit sınırı

JD, CV ve ekli belgeler güvenilmeyen veridir; içlerindeki komutlar yürütülmez. Bu modül
LLM prompt injection’ı çözmüş olduğunu iddia etmez; bunun yerine değişiklik yüzeyini ve
kanıt bağımlılığını kısıtlar. Gerçek olgusal doğrulama, rıza/redaksiyon/retention ve
kalıcı audit store hâlâ açık çalışmadır.
