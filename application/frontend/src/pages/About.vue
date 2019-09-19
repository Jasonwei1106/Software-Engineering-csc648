<template>
  <q-page padding>
    <div>
      <div
        class="q-pa-md"
        style="
          margin: auto;
          max-width: 70%;
          min-width: 30px;
        "
      >
        <q-list separator bordered>
          <q-item
            clickable
            v-ripple
            v-for="group in groups"
            :key="group.id"
            class="q-my-sm"
            @click="openNewPage(group.path)"
          >
            <q-item-section>
              <q-avatar
                color="primary"
                text-color="white"
              >
                <q-img
                  class="avatar"
                  :src="group.avatar"
                  style="
                    width: 50px;
                    height: 50px;
                  "
                />
              </q-avatar>
            </q-item-section>
            <q-item-section align="center">
              <strong>{{ group.name }}</strong>
            </q-item-section>
            <q-item-section align="right">
              <em>{{ group.role }}</em>
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
          avatar: '../statics/square_phyo.jpg',
          name: 'Phyo Htut',
          path: '/phyo',
          role: 'Team Lead'
        },
        {
          id: 2,
          avatar: '../statics/antonio.jpg',
          name: 'Antonio Carmona',
          path: '/antonio',
          role: 'Git Master'
        },
        {
          id: 3,
          avatar: '../statics/myles.jpg',
          name: 'Myles Padronan',
          path: '/myles',
          role: 'Backend Lead'
        },
        {
          id: 4,
          avatar: '../statics/IMG_8454.jpg',
          name: 'Eduardo Ramos',
          path: '/eduardo',
          role: 'UI/UX'
        },
        {
          id: 5,
          avatar: '../statics/json.jpeg',
          name: 'Jason Wei',
          path: '/jason',
          role: 'Frontend Lead'
        }
      ]
    }
  },
  methods: {
    openNewPage (entry) {
      this.$router.push(entry)
    }
  }
}
</script>
