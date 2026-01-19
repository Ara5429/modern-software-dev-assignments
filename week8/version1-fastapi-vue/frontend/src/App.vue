<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <h1 class="text-3xl font-bold text-gray-900">Mood Tracking Notes</h1>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Left Column: Notes and Action Items -->
        <div class="lg:col-span-2 space-y-6">
          <NotesList />
        </div>

        <!-- Right Column: Mood Tracker and Chart -->
        <div class="space-y-6">
          <MoodTracker />
          <MoodChart />
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import NotesList from './components/NotesList.vue'
import MoodTracker from './components/MoodTracker.vue'
import MoodChart from './components/MoodChart.vue'
</script>
