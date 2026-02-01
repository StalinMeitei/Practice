import { useEffect, useRef } from 'react'
import * as d3 from 'd3'
import { Box, Typography } from '@mui/material'

export default function MessageHeatmap({ data, width = 800, height = 300, granularity = 'weekly' }) {
  const svgRef = useRef()

  useEffect(() => {
    // Clear previous content
    d3.select(svgRef.current).selectAll('*').remove()

    // Check if we have data
    const hasData = data && data.length > 0
    
    // Adjust margins based on granularity
    const margin = granularity === 'hourly' 
      ? { top: 40, right: 30, bottom: 30, left: 60 }
      : { top: 40, right: 30, bottom: 30, left: 80 }
    
    const innerWidth = width - margin.left - margin.right
    const innerHeight = height - margin.top - margin.bottom

    // Create SVG
    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .attr('viewBox', `0 0 ${width} ${height}`)
      .attr('style', 'max-width: 100%; height: auto;')

    const g = svg.append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`)

    // Define empty template structure based on granularity
    let xValues, yValues, xLabel, yLabel, emptyData = []
    
    if (granularity === 'hourly') {
      xValues = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
      yValues = Array.from({length: 24}, (_, i) => i)
      xLabel = 'Day'
      yLabel = 'Hour'
      if (!hasData) {
        xValues.forEach(day => {
          yValues.forEach(hour => {
            emptyData.push({ day, hour, total: 0, success: 0, failed: 0 })
          })
        })
      }
    } else if (granularity === 'daily') {
      xValues = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
      yValues = Array.from({length: 31}, (_, i) => i + 1)
      xLabel = 'Month'
      yLabel = 'Day'
      if (!hasData) {
        xValues.forEach(month => {
          yValues.forEach(day => {
            emptyData.push({ month, day, total: 0, success: 0, failed: 0 })
          })
        })
      }
    } else if (granularity === 'weekly') {
      xValues = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
      yValues = [1, 2, 3, 4, 5]
      xLabel = 'Month'
      yLabel = 'Week'
      if (!hasData) {
        xValues.forEach(month => {
          yValues.forEach(week => {
            emptyData.push({ month, week, total: 0, success: 0, failed: 0 })
          })
        })
      }
    } else if (granularity === 'monthly') {
      const currentYear = new Date().getFullYear()
      xValues = Array.from({length: 5}, (_, i) => String(currentYear - 4 + i))
      yValues = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
      xLabel = 'Year'
      yLabel = 'Month'
      if (!hasData) {
        xValues.forEach(year => {
          yValues.forEach(month => {
            emptyData.push({ year, month, total: 0, success: 0, failed: 0 })
          })
        })
      }
    } else if (granularity === 'yearly') {
      const currentYear = new Date().getFullYear()
      xValues = Array.from({length: 10}, (_, i) => String(currentYear - 9 + i))
      yValues = ['Total']
      xLabel = 'Year'
      yLabel = ''
      if (!hasData) {
        xValues.forEach(year => {
          emptyData.push({ year, total: 0, success: 0, failed: 0 })
        })
      }
    }

    // Use actual data if available, otherwise use empty template
    const displayData = hasData ? data : emptyData

    // Get actual x and y values from data if we have it
    if (hasData) {
      if (granularity === 'hourly') {
        xValues = Array.from(new Set(data.map(d => d.day)))
        yValues = Array.from(new Set(data.map(d => d.hour))).sort((a, b) => a - b)
      } else if (granularity === 'daily') {
        xValues = Array.from(new Set(data.map(d => d.month)))
        yValues = Array.from(new Set(data.map(d => d.day))).sort((a, b) => a - b)
      } else if (granularity === 'weekly') {
        xValues = Array.from(new Set(data.map(d => d.month)))
        yValues = Array.from(new Set(data.map(d => d.week))).sort((a, b) => a - b)
      } else if (granularity === 'monthly') {
        xValues = Array.from(new Set(data.map(d => d.year)))
        yValues = Array.from(new Set(data.map(d => d.month)))
      } else if (granularity === 'yearly') {
        xValues = Array.from(new Set(data.map(d => d.year)))
        yValues = ['Total']
      }
    }

    // Create scales
    const xScale = d3.scaleBand()
      .domain(xValues)
      .range([0, innerWidth])
      .padding(0.05)

    const yScale = d3.scaleBand()
      .domain(yValues)
      .range([0, innerHeight])
      .padding(0.05)

    // Color scale based on success rate
    const colorScale = d3.scaleSequential()
      .domain([0, 100])
      .interpolator(d3.interpolateRdYlGn)

    // Create tooltip
    const tooltip = d3.select('body').append('div')
      .attr('class', 'heatmap-tooltip')
      .style('position', 'absolute')
      .style('visibility', 'hidden')
      .style('background-color', 'rgba(0, 0, 0, 0.85)')
      .style('color', 'white')
      .style('padding', '8px 12px')
      .style('border-radius', '4px')
      .style('font-size', '11px')
      .style('pointer-events', 'none')
      .style('z-index', '1000')
      .style('box-shadow', '0 2px 4px rgba(0,0,0,0.2)')

    // Draw cells
    g.selectAll('rect')
      .data(displayData)
      .join('rect')
      .attr('x', d => {
        if (granularity === 'hourly') return xScale(d.day)
        if (granularity === 'daily') return xScale(d.month)
        if (granularity === 'weekly') return xScale(d.month)
        if (granularity === 'monthly') return xScale(d.year)
        if (granularity === 'yearly') return xScale(d.year)
      })
      .attr('y', d => {
        if (granularity === 'hourly') return yScale(d.hour)
        if (granularity === 'daily') return yScale(d.day)
        if (granularity === 'weekly') return yScale(d.week)
        if (granularity === 'monthly') return yScale(d.month)
        if (granularity === 'yearly') return yScale('Total')
      })
      .attr('width', xScale.bandwidth())
      .attr('height', yScale.bandwidth())
      .attr('fill', d => {
        if (d.total === 0) return '#f0f0f0' // Light gray for empty cells
        const successRate = (d.success / d.total) * 100
        return colorScale(successRate)
      })
      .attr('stroke', '#fff')
      .attr('stroke-width', 1)
      .on('mouseover', function(event, d) {
        d3.select(this).attr('stroke', '#333').attr('stroke-width', 2)
        
        let tooltipText = ''
        if (granularity === 'hourly') {
          tooltipText = `${d.day} ${d.hour}:00`
        } else if (granularity === 'daily') {
          tooltipText = `${d.month} ${d.day}`
        } else if (granularity === 'weekly') {
          tooltipText = `${d.month} Week ${d.week}`
        } else if (granularity === 'monthly') {
          tooltipText = `${d.month} ${d.year}`
        } else if (granularity === 'yearly') {
          tooltipText = `${d.year}`
        }
        
        const successRate = d.total > 0 ? ((d.success / d.total) * 100).toFixed(1) : 0
        
        tooltip
          .style('visibility', 'visible')
          .html(`
            <div><strong>${tooltipText}</strong></div>
            <div>Total: ${d.total}</div>
            <div>Success: ${d.success}</div>
            <div>Failed: ${d.failed}</div>
            <div>Success Rate: ${successRate}%</div>
          `)
      })
      .on('mousemove', function(event) {
        tooltip
          .style('top', (event.pageY - 10) + 'px')
          .style('left', (event.pageX + 10) + 'px')
      })
      .on('mouseout', function() {
        d3.select(this).attr('stroke', '#fff').attr('stroke-width', 1)
        tooltip.style('visibility', 'hidden')
      })

    // Add X axis
    g.append('g')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(d3.axisBottom(xScale))
      .selectAll('text')
      .style('font-size', '10px')

    // Add Y axis
    g.append('g')
      .call(d3.axisLeft(yScale))
      .selectAll('text')
      .style('font-size', '10px')

    // Add X axis label
    svg.append('text')
      .attr('x', width / 2)
      .attr('y', height - 5)
      .attr('text-anchor', 'middle')
      .style('font-size', '11px')
      .style('font-weight', '600')
      .text(xLabel)

    // Add Y axis label
    if (yLabel) {
      svg.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('x', -height / 2)
        .attr('y', 15)
        .attr('text-anchor', 'middle')
        .style('font-size', '11px')
        .style('font-weight', '600')
        .text(yLabel)
    }

    // Add title
    svg.append('text')
      .attr('x', width / 2)
      .attr('y', 20)
      .attr('text-anchor', 'middle')
      .style('font-size', '13px')
      .style('font-weight', '600')
      .text(`Message Activity Heatmap (${granularity.charAt(0).toUpperCase() + granularity.slice(1)})`)

    // Cleanup tooltip on unmount
    return () => {
      tooltip.remove()
    }
  }, [data, width, height, granularity])

  return (
    <Box sx={{ position: 'relative' }}>
      <svg ref={svgRef}></svg>
      {(!data || data.length === 0) && (
        <Box
          sx={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            textAlign: 'center',
            pointerEvents: 'none'
          }}
        >
          <Typography variant="body2" color="text.secondary">
            No data available - Send messages to see activity
          </Typography>
        </Box>
      )}
    </Box>
  )
}
