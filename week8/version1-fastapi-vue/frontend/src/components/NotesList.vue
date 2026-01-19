<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-2xl font-semibold text-gray-800">Notes</h2>
      <button
        @click="showCreateModal = true"
        class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
      >
        + New Note
      </button>
    </div>

    <!-- Notes List -->
    <div v-if="loading" class="text-center py-8">
      <p class="text-gray-500">Loading notes...</p>
    </div>
    <div v-else-if="notes.length === 0" class="text-center py-8">
      <p class="text-gray-500">No notes yet. Create your first note!</p>
    </div>
    <div v-else class="space-y-4">
      <div
        v-for="note in notes"
        :key="note.id"
        class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition"
      >
        <div class="flex justify-between items-start mb-2">
          <h3 class="text-lg font-semibold text-gray-800">{{ note.title }}</h3>
          <div class="flex gap-2">
            <button
              @click="editNote(note)"
              class="text-blue-600 hover:text-blue-800"
            >
              Edit
            </button>
            <button
              @click="deleteNote(note.id)"
              class="text-red-600 hover:text-red-800"
            >
              Delete
            </button>
          </div>
        </div>
        <p class="text-gray-600 mb-2">{{ note.content }}</p>
        <div class="flex items-center gap-4 text-sm text-gray-500">
          <span v-if="note.mood_entry" class="flex items-center gap-1">
            <span class="font-semibold">Mood:</span>
            <span
              class="px-2 py-1 rounded"
              :class="getMoodColorClass(note.mood_entry.mood)"
            >
              {{ note.mood_entry.mood }}
            </span>
          </span>
          <span v-if="note.tags && note.tags.length > 0" class="flex items-center gap-2">
            <span class="font-semibold">Tags:</span>
            <span
              v-for="tag in note.tags"
              :key="tag.id"
              class="px-2 py-1 rounded text-white text-xs"
              :style="{ backgroundColor: tag.color }"
            >
              {{ tag.name }}
            </span>
          </span>
        </div>
        <p class="text-xs text-gray-400 mt-2">
          {{ formatDate(note.created_at) }}
        </p>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div
      v-if="showCreateModal || editingNote"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-lg p-6 w-full max-w-md" @click.stop>
        <h3 class="text-xl font-semibold mb-4">
          {{ editingNote ? 'Edit Note' : 'Create Note' }}
        </h3>
        <form @submit.prevent="saveNote" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Title
            </label>
            <input
              v-model="noteForm.title"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Content
            </label>
            <textarea
              v-model="noteForm.content"
              rows="4"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            ></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Mood
            </label>
            <select
              v-model="noteForm.selectedMood"
              :disabled="loadingMoods"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
            >
              <option :value="null">No mood</option>
              <option
                v-for="mood in moodOptions"
                :key="mood.value"
                :value="mood.value"
              >
                {{ mood.label }}
              </option>
            </select>
            <p v-if="loadingMoods" class="text-xs text-gray-500 mt-1">Loading moods...</p>
            <p v-if="moodError" class="text-xs text-red-500 mt-1">{{ moodError }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Tags
            </label>
            <div class="flex flex-wrap gap-2 mb-2">
              <span
                v-for="tag in availableTags"
                :key="tag.id"
                class="px-3 py-1 rounded-full text-sm cursor-pointer"
                :class="isTagSelected(tag.id) ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'"
                @click="toggleTag(tag.id)"
              >
                {{ tag.name }}
              </span>
            </div>
          </div>
          <div v-if="saveError" class="bg-red-50 border border-red-200 rounded-lg p-3">
            <p class="text-sm text-red-600">{{ saveError }}</p>
          </div>
          <div class="flex gap-2 justify-end">
            <button
              type="button"
              @click="closeModal"
              :disabled="saving"
              class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="saving || !isFormValid"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="saving">Saving...</span>
              <span v-else>{{ editingNote ? 'Update' : 'Create' }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { notesAPI, moodsAPI, tagsAPI } from '../api'

const notes = ref([])
const moods = ref([])
const availableTags = ref([])
const loading = ref(true)
const loadingMoods = ref(false)
const saving = ref(false)
const showCreateModal = ref(false)
const editingNote = ref(null)
const moodError = ref('')
const saveError = ref('')
const noteForm = ref({
  title: '',
  content: '',
  selectedMood: null, // Store the mood value (happy, neutral, etc.)
  mood_id: null, // Will be set after creating mood entry
  tag_ids: [],
})

// Predefined mood options with emojis
const moodOptions = [
  { value: 'happy', label: '😊 Happy', emoji: '😊' },
  { value: 'neutral', label: '😐 Neutral', emoji: '😐' },
  { value: 'sad', label: '😢 Sad', emoji: '😢' },
  { value: 'angry', label: '😡 Angry', emoji: '😡' },
  { value: 'tired', label: '😴 Tired', emoji: '😴' }
]

// Computed property for form validation
const isFormValid = computed(() => {
  return noteForm.value.title.trim().length > 0
})

const loadNotes = async () => {
  try {
    const response = await notesAPI.getAll()
    notes.value = response.data
  } catch (error) {
    console.error('Error loading notes:', error)
  }
}

const loadMoods = async () => {
  loadingMoods.value = true
  moodError.value = ''
  try {
    const response = await moodsAPI.getAll()
    moods.value = response.data
  } catch (error) {
    console.error('Error loading moods:', error)
    moodError.value = 'Failed to load moods. You can still create notes without a mood.'
  } finally {
    loadingMoods.value = false
  }
}

const loadTags = async () => {
  try {
    const response = await tagsAPI.getAll()
    availableTags.value = response.data
  } catch (error) {
    console.error('Error loading tags:', error)
  }
}

const saveNote = async () => {
  // Validation
  if (!isFormValid.value) {
    saveError.value = 'Please enter a title for the note.'
    return
  }

  saving.value = true
  saveError.value = ''

  try {
    let moodId = null

    // Check if mood changed when editing
    const isEditing = !!editingNote.value
    const currentMood = editingNote.value?.mood_entry?.mood || null
    const moodChanged = isEditing && currentMood !== noteForm.value.selectedMood

    // If a mood is selected and (creating new note or mood changed), create a mood entry
    if (noteForm.value.selectedMood && (!isEditing || moodChanged)) {
      try {
        const moodResponse = await moodsAPI.create({
          mood: noteForm.value.selectedMood,
          date: new Date().toISOString(),
          note_id: null // Will be set after note is created
        })
        moodId = moodResponse.data.id
      } catch (error) {
        console.error('Error creating mood entry:', error)
        const errorMessage = error.response?.data?.detail || 'Failed to create mood entry'
        saveError.value = `Error creating mood: ${errorMessage}`
        saving.value = false
        return
      }
    } else if (isEditing && !moodChanged) {
      // Keep existing mood_id if mood hasn't changed
      moodId = editingNote.value.mood_id
    }

    const data = {
      title: noteForm.value.title.trim(),
      content: noteForm.value.content.trim() || null,
      mood_id: moodId,
      tag_ids: noteForm.value.tag_ids,
    }

    if (editingNote.value) {
      await notesAPI.update(editingNote.value.id, data)
    } else {
      await notesAPI.create(data)
    }

    await loadNotes()
    closeModal()
  } catch (error) {
    console.error('Error saving note:', error)
    const errorMessage = error.response?.data?.detail || 'Failed to save note. Please try again.'
    saveError.value = errorMessage
  } finally {
    saving.value = false
  }
}

const editNote = (note) => {
  editingNote.value = note
  // Extract mood value from mood_entry if it exists
  const selectedMood = note.mood_entry ? note.mood_entry.mood : null
  noteForm.value = {
    title: note.title,
    content: note.content || '',
    selectedMood: selectedMood,
    mood_id: note.mood_id,
    tag_ids: note.tags ? note.tags.map(t => t.id) : [],
  }
}

const deleteNote = async (id) => {
  if (!confirm('Are you sure you want to delete this note?')) return

  try {
    await notesAPI.delete(id)
    await loadNotes()
  } catch (error) {
    console.error('Error deleting note:', error)
    alert('Error deleting note. Please try again.')
  }
}

const closeModal = () => {
  showCreateModal.value = false
  editingNote.value = null
  saveError.value = ''
  moodError.value = ''
  noteForm.value = {
    title: '',
    content: '',
    selectedMood: null,
    mood_id: null,
    tag_ids: [],
  }
}

const toggleTag = (tagId) => {
  const index = noteForm.value.tag_ids.indexOf(tagId)
  if (index > -1) {
    noteForm.value.tag_ids.splice(index, 1)
  } else {
    noteForm.value.tag_ids.push(tagId)
  }
}

const isTagSelected = (tagId) => {
  return noteForm.value.tag_ids.includes(tagId)
}

const getMoodColorClass = (mood) => {
  const colors = {
    happy: 'bg-yellow-100 text-yellow-800',
    neutral: 'bg-gray-100 text-gray-800',
    sad: 'bg-blue-100 text-blue-800',
    angry: 'bg-red-100 text-red-800',
    tired: 'bg-purple-100 text-purple-800',
  }
  return colors[mood] || 'bg-gray-100 text-gray-800'
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

onMounted(async () => {
  loading.value = true
  await Promise.all([loadNotes(), loadMoods(), loadTags()])
  loading.value = false
})
</script>
