<template>
  <DefaultLayout>
    <div class="max-w-7xl mx-auto py-12 lg:py-16 px-4">
      <div class="flex flex-col lg:flex-row gap-8 items-start lg:items-center justify-between mb-12">
        <div>
          <h1 class="text-5xl font-black bg-gradient-to-r from-gray-900 to-gray-700 dark:from-white dark:to-gray-400 bg-clip-text text-transparent mb-3 tracking-tight">Knowtionaries</h1>
          <p class="text-xl text-gray-500 dark:text-gray-400 font-medium">Domina cualquier tema con tests inteligentes.</p>
        </div>
        <button @click="showCreateModal = true" class="bg-gradient-to-r from-purple-600 to-indigo-600 dark:from-purple-500 dark:to-indigo-500 text-white px-8 py-4 rounded-2xl font-bold shadow-xl hover:shadow-2xl hover:-translate-y-1 transition-all whitespace-nowrap">
          + Nuevo Knowtionary
        </button>
      </div>


      <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 mb-8 border border-gray-100 dark:border-gray-700">
        <div class="flex flex-col lg:flex-row gap-4 items-center lg:items-end">
          <div class="relative flex-1 max-w-md w-full">
            <input v-model="searchTerm" placeholder="Buscar knowtionaries..." class="w-full pl-12 pr-4 py-4 border border-gray-200 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-2xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500 text-lg transition-colors">
            <svg class="w-6 h-6 text-gray-400 dark:text-gray-500 absolute left-4 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <div class="flex gap-2">
            <button @click="filterType = 'all'" :class="['px-6 py-3 rounded-xl font-semibold transition-all', filterType === 'all' ? 'bg-gradient-to-r from-purple-500 to-indigo-500 text-white shadow-lg' : 'bg-gray-100 dark:bg-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600']">
              Todos
            </button>
            <button @click="filterType = 'favorites'" :class="['flex items-center gap-2 px-6 py-3 rounded-xl font-semibold transition-all', filterType === 'favorites' ? 'bg-amber-400 text-white shadow-lg' : 'bg-gray-100 dark:bg-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 hover:text-amber-500 dark:hover:text-amber-400']">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
              </svg>
              Favoritos
            </button>
          </div>
        </div>
      </div>


      <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        <div v-for="quiz in filteredQuizzes" :key="quiz.id" class="group">
          <div :class="['bg-gradient-to-br from-white to-gray-50 dark:from-gray-800 dark:to-gray-900 rounded-3xl p-8 shadow-xl hover:shadow-2xl hover:-translate-y-3 transition-all cursor-pointer border overflow-hidden h-full', quiz.favorite ? 'border-amber-200 dark:border-amber-500/50' : 'border-gray-100 dark:border-gray-700 hover:border-purple-200 dark:hover:border-purple-500/50']" @click="openQuiz(quiz)">
            <div class="relative">

              <div class="absolute top-0 right-0 flex items-center gap-2" @click.stop>
                <button
                  @click="toggleFavorite(quiz)"
                  :class="[
                    'p-2 rounded-xl transition-all duration-200',
                    quiz.favorite
                      ? 'text-amber-400 hover:text-amber-500 hover:bg-amber-50 dark:hover:bg-amber-900/30'
                      : 'text-gray-300 dark:text-gray-600 hover:text-amber-400 hover:bg-amber-50 dark:hover:bg-amber-900/30'
                  ]"
                >
                  <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                  </svg>
                </button>
                <button
                  @click="deleteQuiz(quiz)"
                  :title="confirmingDelete === quiz.id ? 'Confirmar eliminación' : 'Eliminar Knowtionary'"
                  :class="[
                    'p-2 rounded-xl transition-all duration-300',
                    confirmingDelete === quiz.id
                      ? 'bg-red-500 text-white shadow-lg scale-110 animate-pulse'
                      : 'text-gray-300 dark:text-gray-600 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/30'
                  ]"
                >
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path v-if="confirmingDelete !== quiz.id" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                </button>
              </div>
              <div class="w-16 h-16 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-2xl flex items-center justify-center mb-6 shadow-lg group-hover:scale-110 transition-all">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3 line-clamp-2 group-hover:text-purple-600 dark:group-hover:text-purple-400">{{ quiz.name }}</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-4 line-clamp-2 leading-relaxed">{{ quiz.description }}</p>
              <div class="flex items-center gap-4 mb-6 text-sm">
                <span class="px-3 py-1 bg-purple-100 dark:bg-purple-900/50 text-purple-800 dark:text-purple-300 rounded-full font-medium">
                  {{ quiz.questions_count }} preguntas
                </span>
                <span class="px-3 py-1 bg-indigo-100 dark:bg-indigo-900/50 text-indigo-800 dark:text-indigo-300 rounded-full font-medium">
                  {{ Math.round(quiz.avg_score) }}/10
                </span>
              </div>
              <div class="flex items-center justify-between mt-2">
                <span class="text-sm text-gray-500 dark:text-gray-400 font-medium">{{ formatDate(quiz.created_at) }}</span>
                <button class="px-6 py-2 bg-gradient-to-r from-purple-600 to-indigo-600 dark:from-purple-500 dark:to-indigo-500 text-white font-bold rounded-xl shadow hover:shadow-lg transition-all group-hover:scale-105">
                  Jugar Ahora
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="filteredQuizzes.length === 0" class="col-span-full bg-white dark:bg-gray-800 rounded-3xl shadow-lg p-20 flex flex-col items-center justify-center border-2 border-dashed border-gray-300 dark:border-gray-700">
          <div class="w-24 h-24 bg-gradient-to-br from-purple-100 to-indigo-100 dark:from-purple-900/50 dark:to-indigo-900/50 rounded-3xl flex items-center justify-center mb-8">
            <svg class="w-12 h-12 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">{{ searchTerm ? 'Sin resultados' : 'Sin knowtionaries' }}</h3>
          <p class="text-xl text-gray-600 dark:text-gray-400 mb-8 text-center">Crea tu primer Knowtionary interactivo</p>
          <button @click="showCreateModal = true" class="bg-gradient-to-r from-purple-600 to-indigo-600 dark:from-purple-500 dark:to-indigo-500 text-white px-10 py-4 rounded-2xl font-bold shadow-xl hover:shadow-2xl transition-all">
            Crear Knowtionary
          </button>
        </div>
      </div>


      <div v-if="showCreateModal" class="fixed inset-0 bg-black/60 dark:bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-6">
        <div class="bg-white dark:bg-gray-800 rounded-3xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
          <div class="p-8">
            <div class="flex items-center justify-between mb-8">
              <h2 class="text-3xl font-black text-gray-900 dark:text-white tracking-tight">Nuevo Knowtionary</h2>
              <button @click="closeCreateModal" class="text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 p-2 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-700">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <form @submit.prevent="createQuiz">
              <div class="space-y-6">
                <div>
                  <label class="block text-lg font-semibold text-gray-900 dark:text-white mb-3">Nombre del Knowtionary *</label>
                  <input v-model="createForm.name" required class="w-full px-6 py-4 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-2xl focus:ring-3 focus:ring-purple-500/20 focus:border-purple-500 text-lg">
                </div>
                <div>
                  <label class="block text-lg font-semibold text-gray-900 dark:text-white mb-3">Descripción</label>
                  <textarea v-model="createForm.description" rows="3" class="w-full px-6 py-4 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-2xl focus:ring-3 focus:ring-purple-500/20 focus:border-purple-500 text-lg resize-vertical"></textarea>
                </div>
                <div>
                  <label class="block text-lg font-semibold text-gray-900 dark:text-white mb-3">Puntuación máxima por pregunta</label>
                  <input v-model.number="createForm.max_score_per_question" type="number" min="1" max="10" class="w-full px-6 py-4 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-2xl focus:ring-3 focus:ring-purple-500/20 focus:border-purple-500 text-lg">
                </div>

                <div class="mt-8 border-t dark:border-gray-700 pt-8">
                  <div class="flex items-center justify-between mb-6">
                    <h3 class="text-2xl font-bold text-gray-900 dark:text-white">Preguntas</h3>
                    <button type="button" @click="addQuestion" class="px-4 py-2 bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 rounded-xl font-bold hover:bg-indigo-100 dark:hover:bg-indigo-900/50 transition-colors">
                      + Añadir Pregunta
                    </button>
                  </div>
                  
                  <div v-for="(q, qIndex) in createForm.questions" :key="qIndex" class="bg-white dark:bg-gray-800 p-6 rounded-2xl mb-6 relative border-2 border-gray-100 dark:border-gray-700 shadow-sm focus-within:border-indigo-300 dark:focus-within:border-indigo-500 transition-all">
                    <button v-if="createForm.questions.length > 1" @click="removeQuestion(qIndex)" type="button" class="absolute top-4 right-4 text-red-400 hover:text-red-600 dark:hover:text-red-400 p-2 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-xl transition-colors">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                    </button>
                    <label class="block text-sm font-bold text-indigo-600 dark:text-indigo-400 uppercase tracking-wider mb-2">Pregunta {{ qIndex + 1 }}</label>
                    <input v-model="q.question" required placeholder="Ej: ¿Cuál es la capital de Francia?" class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 mb-6 bg-gray-50 dark:bg-gray-700 dark:text-white focus:bg-white dark:focus:bg-gray-800 transition-colors">
                    
                    <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">Opciones (selecciona la correcta)</label>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div v-for="(opt, oIndex) in q.options" :key="oIndex" class="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-700 border-2 rounded-xl hover:border-indigo-300 dark:hover:border-indigo-500 transition-all cursor-pointer group" :class="q.correct_option === oIndex ? 'border-emerald-500 dark:border-emerald-400 bg-emerald-50 dark:bg-emerald-900/20 ring-2 ring-emerald-200 dark:ring-emerald-900' : 'border-gray-200 dark:border-gray-600'">
                        <input type="radio" :name="'correct_' + qIndex" :value="oIndex" v-model="q.correct_option" class="w-5 h-5 text-emerald-600 focus:ring-emerald-500 cursor-pointer">
                        <input v-model="q.options[oIndex]" required :placeholder="'Opción ' + (oIndex + 1)" class="flex-1 px-2 py-1 outline-none bg-transparent font-medium group-hover:text-indigo-900 dark:group-hover:text-indigo-300 dark:text-white transition-colors">
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="flex gap-4 justify-end mt-10">
                <button type="button" @click="closeCreateModal" class="px-10 py-4 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-2xl font-semibold hover:bg-gray-50 dark:hover:bg-gray-700 transition-all">
                  Cancelar
                </button>
                <button type="submit" :disabled="creatingQuiz" class="px-10 py-4 bg-gradient-to-r from-purple-600 to-indigo-600 dark:from-purple-500 dark:to-indigo-500 text-white rounded-2xl font-bold shadow-xl hover:shadow-2xl disabled:opacity-50">
                  {{ creatingQuiz ? 'Creando...' : 'Crear Knowtionary' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>


      <div v-if="currentQuiz" class="fixed inset-0 bg-black/60 dark:bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-6">
        <div class="bg-white dark:bg-gray-800 rounded-3xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
          <div class="sticky top-0 bg-white dark:bg-gray-800 p-6 border-b dark:border-gray-700 z-20">
            <div class="flex items-center gap-4">
              <button @click="closeQuiz" class="p-2 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <div class="flex-1">
                <h2 class="text-3xl font-bold text-gray-900 dark:text-white">{{ currentQuiz.name }}</h2>
                <p class="text-lg text-gray-600 dark:text-gray-400">{{ currentQuiz.questions_count }} preguntas</p>
              </div>
              <button @click="startQuiz" :disabled="!currentQuiz.questions.length" class="bg-gradient-to-r from-emerald-500 to-green-600 dark:from-emerald-400 dark:to-green-500 text-white px-8 py-3 rounded-xl font-bold shadow-lg hover:shadow-xl">
                {{ quizStarted ? 'Continuar Quiz' : 'Empezar Quiz' }}
              </button>
            </div>
          </div>
          <div class="p-8">
            <div v-if="!quizStarted" class="text-center py-20">
              <div class="w-32 h-32 mx-auto mb-8 bg-gradient-to-br from-emerald-100 to-green-100 dark:from-emerald-900/50 dark:to-green-900/50 rounded-3xl flex items-center justify-center">
                <svg class="w-16 h-16 text-emerald-600 dark:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Listo para empezar</h3>
              <p class="text-lg text-gray-600 dark:text-gray-400 mb-8">Responde todas las preguntas correctamente para obtener tu puntuación</p>
              <div class="grid grid-cols-2 gap-4 max-w-md mx-auto">
                <div class="text-center p-6 bg-gray-50 dark:bg-gray-700 rounded-xl">
                  <div class="text-3xl font-bold text-indigo-600 dark:text-indigo-400">{{ currentQuiz.questions_count }}</div>
                  <div class="text-sm text-gray-600 dark:text-gray-300">Preguntas</div>
                </div>
                <div class="text-center p-6 bg-gray-50 dark:bg-gray-700 rounded-xl">
                  <div class="text-3xl font-bold text-emerald-600 dark:text-emerald-400">{{ currentQuiz.max_score_per_question || 1 }}</div>
                  <div class="text-sm text-gray-600 dark:text-gray-300">Puntos máx</div>
                </div>
              </div>
            </div>

            <div v-else-if="currentQuestionIndex < currentQuiz.questions.length">
              <div class="flex items-center gap-4 mb-6">
                <div class="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
                  <span class="w-8 h-8 bg-indigo-100 dark:bg-indigo-900/50 rounded-full flex items-center justify-center font-bold text-indigo-700 dark:text-indigo-300 text-xs">{{ currentQuestionIndex + 1 }}</span>
                  <span>de {{ currentQuiz.questions_count }}</span>
                </div>
                <div class="ml-auto">
                  <div class="flex items-center gap-3">
                    <div class="flex items-center gap-2 px-4 py-2 bg-rose-50 dark:bg-rose-900/30 rounded-xl text-rose-600 dark:text-rose-400 font-bold border border-rose-100 dark:border-rose-800">
                      <svg class="w-5 h-5 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                      {{ timeLeft }}s
                    </div>
                    <div class="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 dark:from-indigo-600 dark:to-purple-700 rounded-xl flex items-center justify-center shadow-lg">
                      <span class="text-white font-bold text-lg">{{ currentQuiz.max_score_per_question || 1 }}pts</span>
                    </div>
                  </div>
                </div>
              </div>
              

              <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mb-8 overflow-hidden">
                <div class="bg-rose-500 dark:bg-rose-600 h-full rounded-full transition-all duration-1000 ease-linear" :style="{ width: (timeLeft / maxTime * 100) + '%' }"></div>
              </div>

              <div class="bg-gradient-to-r from-indigo-50 to-purple-50 dark:from-slate-800 dark:to-slate-900 p-8 rounded-3xl border border-indigo-200 dark:border-slate-700 shadow-sm relative overflow-hidden">
                <div class="absolute -top-10 -right-10 w-40 h-40 bg-purple-200 dark:bg-purple-900/20 rounded-full blur-3xl opacity-50"></div>
                <div class="absolute -bottom-10 -left-10 w-40 h-40 bg-indigo-200 dark:bg-indigo-900/20 rounded-full blur-3xl opacity-50"></div>
                
                <h3 class="text-3xl font-bold text-gray-900 dark:text-white mb-8 text-center relative z-10">{{ currentQuiz.questions[currentQuestionIndex].question }}</h3>
                
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 relative z-10">
                  <label v-for="(option, index) in currentQuiz.questions[currentQuestionIndex].options" :key="index" @click="selectAnswerAndNext(index)" class="flex items-center p-6 bg-white dark:bg-gray-800 border-2 border-gray-100 dark:border-gray-600 rounded-2xl hover:border-indigo-400 dark:hover:border-indigo-500 hover:shadow-lg transition-all cursor-pointer group" :class="{ 'border-emerald-500 dark:border-emerald-400 bg-emerald-50 dark:bg-emerald-900/20 ring-4 ring-emerald-200 dark:ring-emerald-900 scale-105 z-10': answers[currentQuestionIndex] === index }">
                    <input type="radio" :value="index" v-model="answers[currentQuestionIndex]" class="sr-only">
                    <span class="w-8 h-8 mr-4 rounded-full border-2 border-gray-300 dark:border-gray-500 flex items-center justify-center text-sm font-bold group-hover:border-indigo-500 dark:group-hover:border-indigo-400 transition-colors" :class="{ 'bg-emerald-500 dark:bg-emerald-500 border-emerald-500 dark:border-emerald-500 text-white': answers[currentQuestionIndex] === index, 'text-gray-500 dark:text-gray-300': answers[currentQuestionIndex] !== index }">
                      {{ String.fromCharCode(65 + index) }}
                    </span>
                    <span class="font-bold text-gray-700 dark:text-gray-200 text-lg group-hover:text-indigo-700 dark:group-hover:text-indigo-400 transition-colors">{{ option }}</span>
                  </label>
                </div>
              </div>
            </div>


            <div v-else class="text-center py-20">
              <div class="w-48 h-48 mx-auto mb-12 relative">
                <svg class="w-full h-full" viewBox="0 0 200 200">
                  <circle cx="100" cy="100" r="85" fill="none" class="stroke-gray-200 dark:stroke-gray-700" stroke-width="15"></circle>
                  <circle cx="100" cy="100" r="85" fill="none" stroke="#10b981" stroke-width="15" stroke-linecap="round" :stroke-dasharray="circumference" :stroke-dashoffset="circumference - progress * circumference / 100" stroke-dasharray="530"></circle>
                </svg>
                <div class="absolute inset-0 flex items-center justify-center">
                  <div class="text-5xl font-black bg-gradient-to-r from-emerald-500 to-green-600 dark:from-emerald-400 dark:to-green-500 bg-clip-text text-transparent">
                    {{ score }}/10
                  </div>
                </div>
              </div>
              <h2 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">¡Resultado obtenido!</h2>
              <p class="text-2xl text-gray-600 dark:text-gray-300 mb-12">{{ scoreText }}</p>
              <div class="max-w-2xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-4 mb-12">
                <div class="bg-emerald-50 dark:bg-emerald-900/30 p-6 rounded-2xl">
                  <div class="text-3xl font-bold text-emerald-600 dark:text-emerald-400 mb-2">{{ correctAnswers }}</div>
                  <div class="text-sm text-emerald-700 dark:text-emerald-300 font-semibold">Correctas</div>
                </div>
                <div class="bg-gray-50 dark:bg-gray-700 p-6 rounded-2xl">
                  <div class="text-3xl font-bold text-gray-900 dark:text-white mb-2">{{ totalQuestions }}</div>
                  <div class="text-sm text-gray-700 dark:text-gray-300 font-semibold">Total</div>
                </div>
              </div>
              <div class="space-x-4">
                <button @click="restartQuiz" class="px-10 py-4 bg-indigo-600 dark:bg-indigo-500 text-white rounded-2xl font-bold hover:bg-indigo-700 dark:hover:bg-indigo-600 shadow-lg">
                  Repetir
                </button>
                <button @click="closeQuiz" class="px-10 py-4 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-2xl font-semibold hover:bg-gray-50 dark:hover:bg-gray-700">
                  Cerrar
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import api from '@/services/api'

interface Quiz {
  id: number
  name: string
  slug: string
  description: string
  questions_count: number
  avg_score: number
  max_score_per_question: number
  questions: Array<{
    question: string
    options: string[]
    correct_option: number
  }>
  is_owner: boolean
  author: string
  created_at: string
  favorite?: boolean
}

interface CreateForm {
  name: string
  description: string
  max_score_per_question: number
  questions: Array<{
    question: string
    options: string[]
    correct_option: number
  }>
}

const router = useRouter()
const route = useRoute()

const quizzes = ref<Quiz[]>([])
const searchTerm = ref('')
const filterType = ref<'all' | 'favorites'>('all')
const showCreateModal = ref(false)
const confirmingDelete = ref<number | null>(null)
const createForm = ref<CreateForm>({
  name: '', description: '', max_score_per_question: 1,
  questions: [{ question: '', options: ['', '', '', ''], correct_option: 0 }]
})
const creatingQuiz = ref(false)

const currentQuiz = ref<Quiz | null>(null)
const quizStarted = ref(false)
const currentQuestionIndex = ref(0)
const answers = ref<number[]>([])
const score = ref(0)
const correctAnswers = ref(0)
const totalQuestions = ref(0)
const circumference = 2 * Math.PI * 85
const progress = ref(0)

const timeLeft = ref(0)
const maxTime = 15
let timerInterval: number | null = null

const filteredQuizzes = computed(() => {
  return quizzes.value.filter(quiz => {
    const matchesSearch = quiz.name.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
                          quiz.description.toLowerCase().includes(searchTerm.value.toLowerCase())
    const matchesFilter = filterType.value === 'all' || (filterType.value === 'favorites' && quiz.favorite)
    return matchesSearch && matchesFilter
  })
})

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('es-ES', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  })
}

const scoreText = computed(() => {
  if (score.value >= 9) return '¡Excelente!'
  if (score.value >= 7) return 'Muy bien'
  if (score.value >= 5) return 'Bien'
  if (score.value >= 3) return 'En progreso'
  return 'Sigue practicando'
})

const loadQuizzes = async () => {
  try {
    const response = await api.get('knowtionaries/')
    quizzes.value = response.data
  } catch (error) {
    console.error('Error loading quizzes:', error)
  }
}

const createQuiz = async () => {
  creatingQuiz.value = true
  try {
    const payload: any = {
      name: createForm.value.name,
      description: createForm.value.description,
      max_score_per_question: createForm.value.max_score_per_question,
      questions: createForm.value.questions
    }
    
    if (route.query.library_id) {
      payload.library_id = route.query.library_id
    }
    
    await api.post('knowtionaries/add/', payload)
    await loadQuizzes()
    closeCreateModal()
    if (route.query.library_id) {
      router.push(`/libraries/${route.query.library_id}`)
    }
  } catch (error: any) {
    console.error('Error creating quiz:', error)
    const errorMsg = error.response?.data?.error || 'Error al crear el knowtionary'
    alert(errorMsg)
  } finally {
    creatingQuiz.value = false
  }
}

const toggleFavorite = async (quiz: Quiz) => {
  try {
    const response = await api.post(`knowtionaries/favorite/${quiz.slug}/`)
    const idx = quizzes.value.findIndex(q => q.id === quiz.id)
    if (idx !== -1) quizzes.value[idx] = response.data
  } catch (error) {
    console.error('Error toggling favorite:', error)
  }
}

const deleteQuiz = async (quiz: Quiz) => {
  if (confirmingDelete.value !== quiz.id) {
    confirmingDelete.value = quiz.id
    setTimeout(() => {
      if (confirmingDelete.value === quiz.id) confirmingDelete.value = null
    }, 3000)
    return
  }
  try {
    await api.post(`knowtionaries/delete/${quiz.slug}/`)
    quizzes.value = quizzes.value.filter(q => q.id !== quiz.id)
    confirmingDelete.value = null
  } catch (error) {
    console.error('Error deleting quiz:', error)
  }
}

const addQuestion = () => {
  createForm.value.questions.push({
    question: '',
    options: ['', '', '', ''],
    correct_option: 0
  })
}

const removeQuestion = (index: number) => {
  createForm.value.questions.splice(index, 1)
}

const closeCreateModal = () => {
  createForm.value = {
    name: '', description: '', max_score_per_question: 1,
    questions: [{ question: '', options: ['', '', '', ''], correct_option: 0 }]
  }
  showCreateModal.value = false
}

const openQuiz = (quiz: Quiz) => {
  currentQuiz.value = quiz
  currentQuestionIndex.value = 0
  answers.value = []
  quizStarted.value = false
}

const closeQuiz = () => {
  if (timerInterval) clearInterval(timerInterval)
  currentQuiz.value = null
  quizStarted.value = false
  answers.value = []
  currentQuestionIndex.value = 0
}

const startTimer = () => {
  timeLeft.value = maxTime
  if (timerInterval) clearInterval(timerInterval)
  timerInterval = window.setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--
    } else {

      clearInterval(timerInterval)
      if (answers.value[currentQuestionIndex.value] === -1) {
        answers.value[currentQuestionIndex.value] = -2
      }
      if (currentQuestionIndex.value === currentQuiz.value!.questions.length - 1) {
        finishQuiz()
      } else {
        nextQuestion()
      }
    }
  }, 1000)
}

const startQuiz = () => {
  quizStarted.value = true
  totalQuestions.value = currentQuiz.value!.questions.length
  answers.value = new Array(totalQuestions.value).fill(-1)
  startTimer()
}

const selectAnswerAndNext = (index: number) => {
  answers.value[currentQuestionIndex.value] = index
  setTimeout(() => {
    if (currentQuestionIndex.value === currentQuiz.value!.questions.length - 1) {
      finishQuiz()
    } else {
      nextQuestion()
    }
  }, 800)
}

const nextQuestion = () => {
  if (currentQuestionIndex.value < currentQuiz.value!.questions.length - 1) {
    currentQuestionIndex.value++
    startTimer()
  } else {
    finishQuiz()
  }
}

const finishQuiz = () => {
  if (timerInterval) clearInterval(timerInterval)
  currentQuestionIndex.value++
  calculateScore()
}

const restartQuiz = () => {
  currentQuestionIndex.value = 0
  answers.value = []
  quizStarted.value = true
  startTimer()
}

const calculateScore = () => {
  let totalScore = 0
  let correct = 0
  
  currentQuiz.value.questions.forEach((q, index) => {
    if (answers.value[index] === q.correct_option) {
      totalScore += currentQuiz.value.max_score_per_question || 1
      correct++
    }
  })
  
  score.value = Math.round((totalScore / (currentQuiz.value.questions.length * (currentQuiz.value.max_score_per_question || 1))) * 10)
  correctAnswers.value = correct
  progress.value = (score.value / 10) * 100
}

onMounted(() => {
  loadQuizzes()
  if (route.query.library_id) {
    showCreateModal.value = true
  }
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
</style>

