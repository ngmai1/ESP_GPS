import folium

# Sample data for Hue City, Vietnam
data = [
    {"name": "Imperial City", "latitude": 16.4637, "longitude": 107.5909},
    {"name": "Perfume River", "latitude": 16.4637, "longitude": 107.5855},
    {"name": "Dong Ba Market", "latitude": 16.4690, "longitude": 107.5944}
]

# Center the map on the first location
center = [16.4637, 107.5909]

# Create a map centered around the first location with a higher zoom level
map = folium.Map(location=center, zoom_start=16)

# Add points to the map
for location in data:
    folium.Marker([location['latitude'], location['longitude']], popup=f"Location: {location['name']}").add_to(map)

# Save the map to an HTML file
map.save('map.html')

# Read the generated map.html file
with open('map.html', 'r') as file:
    map_html = file.read()

# JavaScript for auto-refresh
auto_refresh_script = '''
<script type="text/javascript">
    // Function to refresh the page every 60 seconds
    function autoRefresh() {
        setTimeout(function() {
            location.reload();
        }, 30000); // 30000 milliseconds = 60 seconds
    }
    // Call the function when the page loads
    window.onload = autoRefresh;
</script>
'''

# Insert the auto-refresh script before the closing </head> tag
map_html = map_html.replace('</head>', auto_refresh_script + '</head>')

# Save the modified HTML back to the file
with open('map.html', 'w') as file:
    file.write(map_html)
