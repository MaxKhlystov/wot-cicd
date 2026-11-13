<template>
  <div class="layout">
    <header>
      <h1>🎖 TankWorld</h1>
      <nav>
        <button v-for="t in tabs" :key="t.key"
                :class="{ active: tab === t.key }"
                @click="switchTab(t.key)">{{ t.label }}</button>
      </nav>
      <span class="health" :class="healthStatus">{{ healthText }}</span>
    </header>

    <main>
      <section class="add-form">
        <h3>Добавить</h3>
        <form @submit.prevent="createItem">
          <input v-for="f in currentFields" :key="f.name"
                 v-model="form[f.name]"
                 :placeholder="f.placeholder"
                 :type="f.type || 'text'" />
          <button type="submit">Создать</button>
        </form>
        <p v-if="error" class="error">{{ error }}</p>
      </section>

      <section>
        <h3>Список ({{ items.length }})</h3>
        <p v-if="loading">Загрузка…</p>
        <table v-else>
          <thead>
            <tr>
              <th v-for="col in currentColumns" :key="col">{{ col }}</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in items" :key="item.id">
              <td v-for="col in currentColumns" :key="col">{{ item[col] }}</td>
              <td><button class="danger" @click="removeItem(item.id)">Удалить</button></td>
            </tr>
            <tr v-if="!items.length"><td :colspan="currentColumns.length + 1">Пусто</td></tr>
          </tbody>
        </table>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const tab = ref('tanks')
const items = ref([])
const form = ref({})
const loading = ref(false)
const error = ref('')
const healthText = ref('проверка…')
const healthStatus = ref('')

const tabs = [
  { key: 'tanks', label: 'Танки' },
  { key: 'players', label: 'Игроки' },
  { key: 'clans', label: 'Кланы' },
]

const config = {
  tanks: {
    fields: [
      { name: 'name', placeholder: 'Название (T-34-85)' },
      { name: 'nation', placeholder: 'Нация (СССР)' },
      { name: 'tier', placeholder: 'Уровень 1–10', type: 'number' },
      { name: 'damage', placeholder: 'Урон', type: 'number' },
    ],
    columns: ['id', 'name', 'nation', 'tier', 'damage', 'hp'],
  },
  players: {
    fields: [
      { name: 'nickname', placeholder: 'Никнейм' },
      { name: 'level', placeholder: 'Уровень', type: 'number' },
    ],
    columns: ['id', 'nickname', 'level', 'experience', 'credits'],
  },
  clans: {
    fields: [
      { name: 'tag', placeholder: 'Тег (IRK)' },
      { name: 'name', placeholder: 'Название клана' },
    ],
    columns: ['id', 'tag', 'name', 'rating'],
  },
}

const currentFields = computed(() => config[tab.value].fields)
const currentColumns = computed(() => config[tab.value].columns)
const endpoint = computed(() => `/api/${tab.value}/`)

async function load() {
  loading.value = true
  error.value = ''
  try {
    const r = await fetch(endpoint.value)
    if (!r.ok) throw new Error('HTTP ' + r.status)
    items.value = await r.json()
  } catch (e) {
    error.value = 'Не удалось загрузить: ' + e.message + ' (запущен ли Django?)'
  } finally {
    loading.value = false
  }
}

function switchTab(key) {
  tab.value = key
  form.value = {}
  load()
}

async function createItem() {
  error.value = ''
  const body = {}
  for (const f of currentFields.value) {
    if (form.value[f.name] !== undefined && form.value[f.name] !== '') {
      body[f.name] = f.type === 'number' ? Number(form.value[f.name]) : form.value[f.name]
    }
  }
  try {
    const r = await fetch(endpoint.value, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
    if (!r.ok) throw new Error('HTTP ' + r.status)
    form.value = {}
    await load()
  } catch (e) {
    error.value = 'Ошибка создания: ' + e.message
  }
}

async function removeItem(id) {
  await fetch(`${endpoint.value}${id}/`, { method: 'DELETE' })
  await load()
}

onMounted(async () => {
  try {
    const r = await fetch('/api/health')
    const d = await r.json()
    healthText.value = d.status === 'ok' ? 'API: ok' : 'API: проблема'
    healthStatus.value = d.status === 'ok' ? 'ok' : 'bad'
  } catch {
    healthText.value = 'API: недоступен'
    healthStatus.value = 'bad'
  }
  load()
})
</script>

<style scoped>
.layout { max-width: 900px; margin: 0 auto; padding: 20px; }
header { display: flex; align-items: center; gap: 24px; flex-wrap: wrap; }
h1 { margin: 0; font-size: 24px; }
nav { display: flex; gap: 8px; }
button { background: #2b323b; color: #e6e6e6; border: 1px solid #444; padding: 8px 16px; border-radius: 6px; cursor: pointer; }
button.active { background: #d4a017; color: #1b1f24; border-color: #d4a017; font-weight: bold; }
button.danger { background: #6e2b2b; border-color: #944; padding: 4px 10px; }
.health { margin-left: auto; font-size: 14px; }
.health.ok { color: #6f6; }
.health.bad { color: #f66; }
main { margin-top: 24px; display: grid; gap: 24px; }
.add-form form { display: flex; gap: 8px; flex-wrap: wrap; }
input { background: #23282e; border: 1px solid #444; color: #e6e6e6; padding: 8px; border-radius: 6px; }
table { width: 100%; border-collapse: collapse; }
th, td { border-bottom: 1px solid #333; padding: 8px; text-align: left; font-size: 14px; }
.error { color: #f66; }
</style>
