HOST="https://hack0425.north.internal.cohere.com/api"

# TODO: This login strategy will change when SSO is fully set up
# As of now, the TEST_PASSWORD is "1234"*2
COUT=$(curl -X POST "${HOST}/v1/signin" -H "Content-Type: application/json" -d '{"email": "evans@canyouhack0425.me", "password": "Evans123"}')

echo "Setting NORTH JWT using: $COUT"
#NORTH_TOKEN=$(echo $COUT | jq -r '.token')
NORTH_TOKEN=$(echo "$COUT" | grep '"token":"' | sed -E 's/.*"token":"([^"]*)".*/\1/')

export MCP_SERVER_URL="https://cohere-hackathon-production.up.railway.app"

curl --location "${HOST}/internal/v1/mcp_servers/delete" \
--header "Content-Type: application/json" \
--header "Authorization: Bearer ${NORTH_TOKEN}" \
--data '{
    "url": '"\"${MCP_SERVER_URL}\""'
}'