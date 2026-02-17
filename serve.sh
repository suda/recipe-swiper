#!/bin/bash
# Quick server to preview the recipe swiper
# Run: ./serve.sh

PORT=8080

echo "🍽️  Recipe Swiper Server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Starting server on http://localhost:$PORT"
echo ""
echo "📱 Open in your browser:"
echo "   http://localhost:$PORT"
echo ""
echo "Press Ctrl+C to stop"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Use Python 3's built-in HTTP server
python3 -m http.server $PORT
