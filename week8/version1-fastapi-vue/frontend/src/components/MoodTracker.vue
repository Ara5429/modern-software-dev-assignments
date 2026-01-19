<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h2 class="text-2xl font-semibold text-gray-800 mb-4">Track Your Mood</h2>

    <div class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Select your mood
        </label>
        <div class="grid grid-cols-2 gap-2">
          <button
            v-for="mood in moodOptions"
            :key="mood.value"
            @click="selectMood(mood.value)"
            class="px-4 py-3 rounded-lg border-2 transition"
            :class="
              selectedMood === mood.value
                ? `${mood.bgColor} ${mood.textColor} border-${mood.borderColor}`
                : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
            "
          >
            <span class="text-2xl mb-1 block">{{ mood.emoji }}</span>
            <span class="text-sm font-medium">{{ mood.label }}</span>
          </button>
        </div>
      </div>

      <div v-if="selectedMood">
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Note (optional)
        </label>
        <textarea
          v-model="moodNote"
          rows="3"
          placeholder="Add a note about your mood..."
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        ></textarea>
      </div>

      <button
        v-if="selectedMood"
        @click="saveMood"
        :disabled="saving"
        class="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
      >
        {{ saving ? 'Saving...' : 'Save Mood' }}
      </button>

      <!-- Recent Moods -->
      <div v-if="recentMoods.length > 0" class="mt-6">
        <h3 class="text-lg font-semibold text-gray-800 mb-2">Recent Moods</h3>
        <div class="space-y-2">
          <div
            v-for="mood in recentMoods.slice(0, 5)"
            :key="mood.id"
            class="flex items-center justify-between p-2 bg-gray-50 rounded"
          >
            <div class="flex items-center gap-2">
              <span class="text-xl">{{ getMoodEmoji(mood.mood) }}</span>
              <span class="text-sm text-gray-700">{{ mood.mood }}</span>
            </div>
            <span class="text-xs text-gray-500">
              {{ formatDate(mood.date) }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { moodsAPI, notesAPI } from '../api'

const moodOptions = [
  { value: 'happy', label: 'Happy', emoji: '😊', bgColor: 'bg-yellow-100', textColor: 'text-yellow-800', borderColor: 'yellow-400' },
  { value: 'neutral', label: 'Neutral', emoji: '😐', bgColor: 'bg-gray-100', textColor: 'text-gray-800', borderColor: 'gray-400' },
  { value: 'sad', label: 'Sad', emoji: '😢', bgColor: 'bg-blue-100', textColor: 'text-blue-800', borderColor: 'blue-400' },
  { value: 'angry', label: 'Angry', emoji: '😠', bgColor: 'bg-red-100', textColor: 'text-red-800', borderColor: 'red-400' },
  { value: 'tired', label: 'Tired', emoji: '😴', bgColor: 'bg-purple-100', textColor: 'text-purple-800', borderColor: 'purple-400' },
]

const selectedMood = ref(null)
const moodNote = ref('')
const saving = ref(false)
const recentMoods = ref([])

const selectMood = (mood) => {
  selectedMood.value = mood
}

const saveMood = async () => {
  if (!selectedMood.value) return

  saving.value = true
  try {
    let noteId = null

    // Create note if there's content
    if (moodNote.value.trim()) {
      const noteResponse = await notesAPI.create({
        title: `Mood: ${selectedMood.value}`,
        content: moodNote.value,
        tag_ids: [],
      })
      noteId = noteResponse.data.id
    }

    // Create mood entry
    await moodsAPI.create({
      mood: selectedMood.value,
      note_id: noteId,
    })

    // Reset form
    selectedMood.value = null
    moodNote.value = ''

    // Reload recent moods
    await loadRecentMoods()

    // Emit event to refresh chart
    window.dispatchEvent(new CustomEvent('mood-saved'))
  } catch (error) {
    console.error('Error saving mood:', error)
    alert('Error saving mood. Please try again.')
  } finally {
    saving.value = false
  }
}

const loadRecentMoods = async () => {
  try {
    const response = await moodsAPI.getAll()
    recentMoods.value = response.data.slice(0, 10)
  } catch (error) {
    console.error('Error loading recent moods:', error)
  }
}

const getMoodEmoji = (mood) => {
  const moodOption = moodOptions.find(m => m.value === mood)
  return moodOption ? moodOption.emoji : '😐'
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 0) {
    return 'Today'
  } else if (diffDays === 1) {
    return 'Yesterday'
  } else {
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  }
}

onMounted(async () => {
  await loadRecentMoods()
  
  // Listen for mood saved events
  window.addEventListener('mood-saved', loadRecentMoods)
})
</script>
