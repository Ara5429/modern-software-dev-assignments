<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h2 class="text-2xl font-semibold text-gray-800 mb-4">Weekly Mood Chart</h2>
    
    <div v-if="loading" class="text-center py-8">
      <p class="text-gray-500">Loading chart data...</p>
    </div>
    <div v-else-if="chartData.labels.length === 0" class="text-center py-8">
      <p class="text-gray-500">No mood data available yet. Start tracking your mood!</p>
    </div>
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Chart, registerables } from 'chart.js'
import { moodsAPI } from '../api'

Chart.register(...registerables)

const chartCanvas = ref(null)
const loading = ref(true)
const chartInstance = ref(null)
const chartData = ref({
  labels: [],
  datasets: [{
    label: 'Mood',
    data: [],
    borderColor: 'rgb(59, 130, 246)',
    backgroundColor: 'rgba(59, 130, 246, 0.1)',
    tension: 0.4,
  }],
})

const moodValues = {
  happy: 5,
  neutral: 3,
  sad: 1,
  angry: 2,
  tired: 2.5,
}

const loadChartData = async () => {
  try {
    loading.value = true
    const response = await moodsAPI.getWeekly()
    const moods = response.data

    // Group moods by date
    const moodsByDate = {}
    moods.forEach(mood => {
      const dateObj = new Date(mood.date)
      const dateKey = dateObj.toISOString().split('T')[0] // Use YYYY-MM-DD as key
      if (!moodsByDate[dateKey]) {
        moodsByDate[dateKey] = []
      }
      moodsByDate[dateKey].push(moodValues[mood.mood] || 3)
    })

    // Calculate average mood per day and sort by date
    const sortedDates = Object.keys(moodsByDate).sort()
    const labels = sortedDates.map(dateKey => {
      const dateObj = new Date(dateKey)
      return dateObj.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
      })
    })
    const data = sortedDates.map(dateKey => {
      const dayMoods = moodsByDate[dateKey]
      const avg = dayMoods.reduce((sum, val) => sum + val, 0) / dayMoods.length
      return avg.toFixed(1)
    })

    chartData.value = {
      labels,
      datasets: [{
        label: 'Average Mood (1=Low, 5=High)',
        data,
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4,
        fill: true,
      }],
    }

    updateChart()
  } catch (error) {
    console.error('Error loading chart data:', error)
  } finally {
    loading.value = false
  }
}

const updateChart = () => {
  if (!chartCanvas.value) return

  if (chartInstance.value) {
    chartInstance.value.destroy()
  }

  chartInstance.value = new Chart(chartCanvas.value, {
    type: 'line',
    data: chartData.value,
    options: {
      responsive: true,
      maintainAspectRatio: true,
      scales: {
        y: {
          beginAtZero: false,
          min: 1,
          max: 5,
          ticks: {
            stepSize: 0.5,
            callback: function(value) {
              const moodMap = {
                5: 'Happy',
                3: 'Neutral',
                1: 'Sad',
                2: 'Angry',
                2.5: 'Tired',
              }
              return moodMap[value] || value
            },
          },
        },
      },
      plugins: {
        legend: {
          display: true,
          position: 'top',
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              return `Mood: ${context.parsed.y}`
            },
          },
        },
      },
    },
  })
}

const handleMoodSaved = () => {
  loadChartData()
}

onMounted(async () => {
  await loadChartData()
  window.addEventListener('mood-saved', handleMoodSaved)
})

onUnmounted(() => {
  if (chartInstance.value) {
    chartInstance.value.destroy()
  }
  window.removeEventListener('mood-saved', handleMoodSaved)
})
</script>
