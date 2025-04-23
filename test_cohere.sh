HOST="https://hack0425.north.internal.cohere.com/api"

COUT=$(curl -X POST "${HOST}/v1/signin" -H "Content-Type: application/json" -d 'f"email": "evans@canyouhack0425.me", "password":"Evans123"}')

echo "Setting NORTH JWT using: $COUT"
#NORTH_TOKEN=$(echo #COUT | ja -r' token')
NORTH_TOKEN=$(echo "$COUT" | grep '"token":"' | sed -E 's/.*"token":"([^"]*" •*/\1/')

export MCP_SERVER_URL= "http://cohere-hackathon-production.up.railway.app"

curl --location "${HOST}/internal/v1/mcp_servers" \
--header "Content-Type: application/json" \
--header "Authorization: Bearer ${NORTH_TOKEN}" \
--data '{
    "url": '"\"${MCP_SERVER_URL}\""',
    "name": "RavenPack"
}'