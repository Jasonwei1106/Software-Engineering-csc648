<template>
  <q-page padding>
<div>
        <div class="q-pa-md"
        style="max-width: 350px margin : 0 auto;
        padding-left: 300px;
        padding-right: 300px;"
        >
        <q-list bordered>
          <q-item
            clickable
            v-ripple
            v-for="group in groups"
            :key="group.id"
            class="q-my-sm"
            @click="openNewPage(group.name)"
          >
            <q-item-section>
              <q-avatar
                color="primary"
                text-color="white"
              >
                {{ group.letter }}
              </q-avatar>
            </q-item-section>
            <q-item-section>
              <q-item-label>
                {{ group.name }}
              </q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-icon name="chat_bubble" color="green" ></q-icon>
            </q-item-section>
          </q-item>
          </q-list>
        </div>
        </div>
  </q-page>
</template>

<script>
export default {
  data () {
    return {
      groups: [
        {
          id: 1,
          letter: 'P',
          name: 'Phyo'

        },
        {
          id: 2,
          letter: 'A',
          name: 'Antonio'
        },
        {
          id: 3,
          letter: 'M',
          name: 'Myles'
        },
        {
          id: 4,
          letter: 'E',
          name: 'Eduardo'
        },
        {
          id: 5,
          letter: 'J',
          name: 'Jason'
        }
      ]
    }
  },
  methods: {
    openNewPage (entry) {
      let route = entry.toLowerCase()
      console.log(route)
      this.$router.push(`/${route}`)
      // window.open(entry, '_blank')
    }
  }
}
</script>
