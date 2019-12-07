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
            clickable v-ripple
            v-for="(group, ind) in groups"
            :key="ind"
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
                  style="width: 50px; height: 50px;"
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
          avatar: '../statics/square_phyo.jpg',
          name: 'Phyo Htut',
          path: '/about/phyo',
          role: 'Team Lead'
        },
        {
          avatar: '../statics/antonio.jpg',
          name: 'Antonio Carmona',
          path: '/about/antonio',
          role: 'Git Master'
        },
        {
          avatar: '../statics/myles.jpg',
          name: 'Myles Padronan',
          path: '/about/myles',
          role: 'Backend Lead'
        },
        {
          avatar: '../statics/IMG_8454.jpg',
          name: 'Eduardo Ramos',
          path: '/about/eduardo',
          role: 'UI/UX'
        },
        {
          avatar: '../statics/json.jpeg',
          name: 'Jason Wei',
          path: '/about/jason',
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

<style lang="stylus">

</style>
