#!/bin/bash
# Quick Dashboard Launcher for Buildly Labs Foundry
# Generates and opens the automation dashboard

echo "🚀 Buildly Labs Foundry - Dashboard Launcher"
echo "============================================="

# Generate fresh dashboard
echo "🔄 Generating fresh dashboard data..."
python3 scripts/generate_dashboard.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Dashboard generated successfully!"
    echo ""
    echo "📊 Dashboard features:"
    echo "   • Real automation metrics (day/week/month)"
    echo "   • Environment configuration status"
    echo "   • Outreach performance analytics"
    echo "   • Error logs and system health"
    echo "   • Actionable recommendations"
    echo ""
    
    # Try to open in default browser (macOS)
    if command -v open &> /dev/null; then
        echo "🌐 Opening dashboard in default browser..."
        open automation_dashboard.html
    else
        echo "🌐 Dashboard ready at: file://$(pwd)/automation_dashboard.html"
        echo "   Copy this path to your browser to view"
    fi
    
    echo ""
    echo "💡 Pro tip: Bookmark the dashboard and refresh to see updated metrics"
    echo "🔄 Dashboard auto-refreshes every 5 minutes"
    
else
    echo "❌ Error generating dashboard. Check the logs for details."
    exit 1
fi