import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
import api.index as m
raw=[
 {"id":"A","customer":"C1","region":"North","product":"Kettle","qty":2,"unit_price":10,"amount":20,"currency":"USD","status":"paid","created_at":"2026-03-31T20:00:00Z","updated_at":"2026-04-01T00:00:00Z"},
 {"id":"A","customer":"C1","region":"North","product":"Kettle","qty":2,"unit_price":10,"amount":20,"currency":"USD","status":"refunded","created_at":"2026-03-31T20:00:00Z","updated_at":"2026-04-02T00:00:00Z"},
 {"id":"B","customer":"C2","region":"North","product":"Mixer","qty":1,"unit_price":100,"amount":100,"currency":"EUR","status":"paid","created_at":"2026-03-15T10:00:00+05:30","updated_at":"2026-03-16T00:00:00Z"},
 {"id":"C","customer":"C2","region":"South","product":"Mixer","qty":3,"unit_price":1000,"amount":3000,"currency":"INR","status":"paid","created_at":"2026-03-31T19:00:00Z","updated_at":"2026-03-31T19:00:00Z"},
]
m._cache.update(t=9e18, rows=m.build(raw, {"USD":1,"EUR":1.06,"INR":0.01146}))
for r in m._cache["rows"]: print(r["id"], r["status"], r["date"], round(r["amount_usd"],4))
Q=lambda **k: {"kind":"single","q":k}
print("rev North Mar", m.evaluate(Q(statuses=["paid"],filters={"region":"North"},date_from="2026-03-01",date_to="2026-03-31",measure="sum_usd")))
print("rev Apr all", m.evaluate(Q(statuses=["paid"],date_from="2026-04-01",date_to="2026-04-30",measure="sum_usd")))
print("refunds Apr", m.evaluate(Q(statuses=["refunded"],date_from="2026-04-01",date_to="2026-04-30",measure="sum_usd")))
print("top product rev", m.evaluate(Q(statuses=["paid"],measure="sum_usd",group_by="product",pick="max")))
print("net", m.evaluate({"kind":"difference","a":{"statuses":["paid"],"measure":"sum_usd"},"b":{"statuses":["refunded"],"measure":"sum_usd"}}))
