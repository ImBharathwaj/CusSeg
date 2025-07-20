curl -X POST "http://localhost:8000/webhook/client123" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaGFuYXNla2FyIiwiZXhwIjoxNzUzMDIwODQ5fQ.J87wntSkGvn6U1fvvx9VOYxB7sb-ATT5Ifb98jVSfrU" \
  -H "Content-Type: application/json" \
  -d '{"sensor": "temp", "value": 29, "unit": "C"}'


curl -X POST "http://localhost:8000/webhook/client123" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaGFuYXNla2FyIiwiZXhwIjoxNzUzMDIwODQ5fQ.J87wntSkGvn6U1fvvx9VOYxB7sb-ATT5Ifb98jVSfrU" \
  -H "Content-Type: application/json" \
  -d '{
    "event": "signup",
    "user": {"id": 888, "name": "Bharath"},
    "meta": {"campaign": "summer", "source": "web"}
}'


curl -X POST "http://localhost:8000/webhook/client123" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaGFuYXNla2FyIiwiZXhwIjoxNzUzMDIwODQ5fQ.J87wntSkGvn6U1fvvx9VOYxB7sb-ATT5Ifb98jVSfrU" \
  -H "Content-Type: application/json" \
  -d '[{"foo": "bar"}, {"foo": "baz"}]'

curl -X POST "http://localhost:8000/webhook/client123" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaGFuYXNla2FyIiwiZXhwIjoxNzUzMDIwODQ5fQ.J87wntSkGvn6U1fvvx9VOYxB7sb-ATT5Ifb98jVSfrU" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": 87,
    "success": true,
    "tags": ["urgent", "payment"],
    "details": {"mode": "upi", "amount": 450.75}
}'

curl -X POST "http://localhost:8000/webhook/client123" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaGFuYXNla2FyIiwiZXhwIjoxNzUzMDIwODQ5fQ.J87wntSkGvn6U1fvvx9VOYxB7sb-ATT5Ifb98jVSfrU" \
  -H "Content-Type: application/json" \
  -d '42'

curl -X POST "http://localhost:8000/webhook/client123" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaGFuYXNla2FyIiwiZXhwIjoxNzUzMDIwODQ5fQ.J87wntSkGvn6U1fvvx9VOYxB7sb-ATT5Ifb98jVSfrU" \
  -H "Content-Type: application/json" \
  -d '{"event": "fail", "missing": }'
