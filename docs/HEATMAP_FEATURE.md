# Heatmap Visualization Feature

## 🎉 New Feature: Interactive Message Heatmap

A D3.js-powered heatmap visualization has been added to show message success/failure patterns over time, inspired by the vaccine impact visualization.

---

## 📊 What's New

### Toggle Between Views

The dashboard now includes a toggle button to switch between two visualization modes:

1. **Line Chart** - Shows sent, received, and failed messages over time
2. **Heatmap** - Shows success rate patterns by week and month

### Heatmap Features

- ✅ **Color-coded cells** - Green (high success) to Red (high failure)
- ✅ **Interactive tooltips** - Hover to see detailed statistics
- ✅ **Weekly breakdown** - See patterns by week within each month
- ✅ **12-month view** - Visualize a full year of data
- ✅ **Real-time data** - Fetched from database
- ✅ **Gradient legend** - Shows success rate scale (0-100%)

---

## 🎯 How to Use

### Access the Heatmap

1. **Login** to dashboard: http://192.168.1.200:8001
2. Navigate to **Overview** page
3. Scroll to **Message Trends** section
4. Click the **Heatmap** toggle button

### Toggle Between Views

```
┌─────────────────────────────────────┐
│  Message Trends                     │
│  [Line Chart] [Heatmap] ← Toggle    │
├─────────────────────────────────────┤
│                                     │
│  [Visualization appears here]       │
│                                     │
└─────────────────────────────────────┘
```

### Interact with Heatmap

- **Hover** over cells to see:
  - Month and week
  - Total messages
  - Success count and percentage
  - Failed count

- **Color interpretation**:
  - 🟢 **Green** - High success rate (80-100%)
  - 🟡 **Yellow** - Medium success rate (50-80%)
  - 🔴 **Red** - Low success rate (0-50%)
  - ⚪ **Gray** - No data

---

## 📈 Visualization Details

### Heatmap Layout

```
                Message Success Rate Heatmap
                                                    [0% ──────── 100%]
                                                    [Red → Yellow → Green]

        Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec
Week 1  [█]  [█]  [█]  [█]  [█]  [█]  [█]  [█]  [█]  [█]  [█]  [█]
Week 2  [█]  [█]  [█]  [█]  [█]  [█]  [█]  [█]  [█]  [█]  [█]  [█]
Week 3  [█]  [█]  [█]  [█]  [█]  [█]  [█]  [█]  [█]  [█]  [█]  [█]
Week 4  [█]  [█]  [█]  [█]  [█]  [█]  [█]  [█]  [█]  [█]  [█]  [█]
Week 5  [█]  [█]  [█]  [█]  [█]  [█]  [█]  [█]  [█]  [█]  [█]  [█]
```

### Color Scale

The heatmap uses D3's `interpolateRdYlGn` color scale:

- **0%** success → 🔴 Red (#EF4444)
- **50%** success → 🟡 Yellow (#F59E0B)
- **100%** success → 🟢 Green (#10B981)

### Data Granularity

- **X-axis**: 12 months (Jan - Dec)
- **Y-axis**: Weeks (1-5 per month)
- **Cell value**: Success rate percentage
- **Tooltip**: Detailed statistics

---

## 🔧 Technical Implementation

### Frontend Components

**New Component**: `MessageHeatmap.jsx`
- Built with D3.js
- SVG-based visualization
- Responsive design
- Interactive tooltips

**Updated Component**: `Dashboard.jsx`
- Added toggle button group
- State management for view switching
- Heatmap data fetching

### Backend API

**New Endpoint**: `/api/heatmap-data/`

**Request**:
```http
GET /api/heatmap-data/
```

**Response**:
```json
{
  "heatmapData": [
    {
      "month": "Jan",
      "week": 1,
      "total": 45,
      "success": 42,
      "failed": 3
    },
    {
      "month": "Jan",
      "week": 2,
      "total": 38,
      "success": 35,
      "failed": 3
    },
    ...
  ]
}
```

### Data Processing

The backend calculates:
1. **Week boundaries** - Start and end dates for each week
2. **Message counts** - Total, success, failed per week
3. **Success rate** - Calculated as (success / total) * 100

### D3.js Features Used

- `d3.scaleBand()` - For X and Y axes
- `d3.scaleSequential()` - For color scale
- `d3.interpolateRdYlGn()` - Red-Yellow-Green gradient
- `d3.select()` - DOM manipulation
- SVG elements - Rectangles, text, axes

---

## 📊 Use Cases

### 1. Identify Problem Periods

**Scenario**: Find when failures spike

**How to use**:
1. Switch to heatmap view
2. Look for red cells
3. Hover to see exact failure counts
4. Investigate those time periods

### 2. Monitor Success Trends

**Scenario**: Track improvement over time

**How to use**:
1. View heatmap
2. Compare recent months to older months
3. Look for color progression (red → yellow → green)

### 3. Weekly Patterns

**Scenario**: Identify weekly patterns

**How to use**:
1. Look at specific weeks across months
2. Check if certain weeks consistently have issues
3. Correlate with business cycles

### 4. Seasonal Analysis

**Scenario**: Understand seasonal variations

**How to use**:
1. Compare summer vs winter months
2. Look for holiday period impacts
3. Plan capacity accordingly

---

## 🎨 Design Specifications

### Dimensions
- **Width**: 900px (responsive)
- **Height**: 400px
- **Margins**: Top 60px, Right 40px, Bottom 40px, Left 100px

### Typography
- **Title**: 16px, bold
- **Axis labels**: 11px
- **Legend**: 10px
- **Tooltip**: 12px

### Colors
- **Success**: #10B981 (Green)
- **Warning**: #F59E0B (Yellow/Orange)
- **Error**: #EF4444 (Red)
- **No data**: #f0f0f0 (Light gray)
- **Cell border**: #fff (White)

### Interactions
- **Hover**: Cell border changes to #333, width 2px
- **Tooltip**: Black background (80% opacity), white text
- **Cursor**: Pointer on hover

---

## 📱 Responsive Design

### Desktop (>960px)
- Full heatmap visible
- All months displayed
- Optimal cell size

### Tablet (600-960px)
- Heatmap scales down
- Maintains aspect ratio
- Scrollable if needed

### Mobile (<600px)
- Horizontal scroll enabled
- Touch-friendly tooltips
- Maintains readability

---

## 🔮 Future Enhancements

### Potential Improvements

1. **Date Range Selector**
   - Choose custom date ranges
   - Compare different periods
   - Year-over-year comparison

2. **Drill-down Capability**
   - Click cell to see message list
   - Filter by week
   - View individual messages

3. **Export Functionality**
   - Export heatmap as PNG
   - Export data as CSV
   - Generate PDF reports

4. **Additional Metrics**
   - Average processing time heatmap
   - Message size heatmap
   - Partner-specific heatmaps

5. **Zoom & Pan**
   - Zoom into specific months
   - Pan across timeline
   - Focus on problem areas

6. **Annotations**
   - Add notes to specific weeks
   - Mark known issues
   - Document incidents

---

## 🧪 Testing

### Visual Testing

1. **Check heatmap renders**
   ```
   - Open dashboard
   - Click Heatmap toggle
   - Verify cells appear
   - Check color gradient
   ```

2. **Test interactions**
   ```
   - Hover over cells
   - Verify tooltip appears
   - Check tooltip content
   - Test cell highlighting
   ```

3. **Test toggle**
   ```
   - Switch to Line Chart
   - Switch back to Heatmap
   - Verify smooth transition
   - Check data persists
   ```

### Data Testing

1. **Verify data accuracy**
   ```bash
   # Test API endpoint
   curl http://192.168.1.200:8001/api/heatmap-data/
   
   # Check response format
   # Verify calculations
   ```

2. **Test edge cases**
   ```
   - No data (empty database)
   - Single message
   - All success
   - All failures
   ```

---

## 📝 API Documentation

### Endpoint: Get Heatmap Data

**URL**: `/api/heatmap-data/`  
**Method**: `GET`  
**Auth**: Not required (for now)

**Response Format**:
```json
{
  "heatmapData": [
    {
      "month": "string",      // Month name (Jan-Dec)
      "week": number,         // Week number (1-5)
      "total": number,        // Total messages
      "success": number,      // Successful messages
      "failed": number        // Failed messages
    }
  ]
}
```

**Success Response** (200):
```json
{
  "heatmapData": [
    {"month": "Jan", "week": 1, "total": 45, "success": 42, "failed": 3},
    {"month": "Jan", "week": 2, "total": 38, "success": 35, "failed": 3}
  ]
}
```

**Error Response** (500):
```json
{
  "error": "Error message"
}
```

---

## 🚀 Deployment

### Files Modified

**Backend**:
- `api_views.py` - Added `get_heatmap_data()` function
- `P1/urls.py` - Added heatmap endpoint route

**Frontend**:
- `frontend/src/components/MessageHeatmap.jsx` - New D3.js component
- `frontend/src/pages/Dashboard.jsx` - Added toggle and heatmap integration
- `frontend/package.json` - Added D3.js dependency

### Deployment Steps

1. **Install D3.js**
   ```bash
   cd frontend
   npm install d3
   ```

2. **Build frontend**
   ```bash
   npm run build
   ```

3. **Deploy to server**
   ```powershell
   .\deploy-heatmap-update.ps1
   ```

4. **Verify deployment**
   ```
   - Open http://192.168.1.200:8001
   - Login to dashboard
   - Check heatmap toggle appears
   - Test both views
   ```

---

## ✅ Summary

**What Was Added**:
- ✅ Toggle button (Line Chart / Heatmap)
- ✅ D3.js heatmap visualization
- ✅ Interactive tooltips
- ✅ Color-coded success rates
- ✅ Weekly breakdown by month
- ✅ Real database integration
- ✅ Gradient legend
- ✅ Responsive design

**Where to Find It**:
- **URL**: http://192.168.1.200:8001
- **Page**: Overview (Dashboard)
- **Section**: Message Trends (bottom)
- **Toggle**: Top-right of chart section

**Benefits**:
- 📊 Better pattern recognition
- 🔍 Easier problem identification
- 📈 Visual trend analysis
- 🎯 Weekly granularity
- 💡 Intuitive color coding

---

**Updated**: January 31, 2026  
**Version**: 1.2  
**Feature**: Heatmap Visualization with Toggle
