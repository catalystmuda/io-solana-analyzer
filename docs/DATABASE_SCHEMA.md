# DATABASE SCHEMA

## Table : token

- mint_address
- name
- symbol
- creator_wallet
- launch_time
- website
- twitter
- telegram
- image
- description

---

## Table : creator

- wallet
- first_seen
- total_token
- success_count
- rug_count
- highest_marketcap
- average_marketcap

---

## Table : holder_snapshot

- mint_address
- timestamp
- total_holder
- top10_percent
- creator_percent
- whale_percent

---

## Table : trading_snapshot

- mint_address
- timestamp
- marketcap
- liquidity
- volume
- buy_count
- sell_count

---

## Table : social_snapshot

- mint_address
- twitter_followers
- twitter_age
- telegram_member
- website_age

---

## Table : score_history

- mint_address
- timestamp
- creator_score
- holder_score
- social_score
- trading_score
- historical_score
- final_score

---

## Table : historical_result

- mint_address
- peak_marketcap
- graduated
- rug
- survival_days