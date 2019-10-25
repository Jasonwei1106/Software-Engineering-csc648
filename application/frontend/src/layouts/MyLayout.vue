<template>
  <q-layout view="hHh lpR fFf">
    <q-header reveal elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn
          :hidden="leftDrawerOpen"
          flat dense round
          aria-label="Menu"
          @click="leftDrawerOpen = !leftDrawerOpen"
          icon="arrow_right"
        />

        <q-space />

        <div
          class="cursor-pointer"
          style="width: 80px;"
          @click="goHome"
        >
          <q-img src="../statics/icons/96p.png" />
        </div>

        <q-space />
        <q-btn stretch flat no-caps label="Log In" @click="icon = true" /> |
        <q-btn stretch flat no-caps label="Sign Up" to="/register" />
        <!-- <div>
        <q-input borderless dense debounce="300" color="primary" v-model="filter" placeholder = "search">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
        </div> -->
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      bordered overlay
      content-class="bg-grey-2"
    >
      <q-list>
        <q-item-label header>
          <div class="row">
            Navigation
            <q-space />
            <q-btn
              flat dense round
              @click="leftDrawerOpen = !leftDrawerOpen"
              icon="close"
            />
          </div>
        </q-item-label>
        <q-item to="/">
          <q-item-section avatar>
            <q-icon name="list" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Home</q-item-label>
          </q-item-section>
        </q-item>
        <q-item to="/about">
          <q-item-section avatar>
            <q-icon name="contacts" />
          </q-item-section>
          <q-item-section>
            <q-item-label>About</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container style="min-height: 90vh;">
      <router-view />
    </q-page-container>

    <div
      class="row"
      style="background-color: #027BE3; height: 100px;"
    >
      <div class="q-pa-md">
        <q-img src="../statics/icons/96p.png" style="width: 70px;" />
      </div>
      <q-space/>
      <div class="q-pa-md" align="center">
        <div class="text-white">
          Follow Us On
        </div>

        <div>
          <q-icon
            class="cursor-pointer"
            name="fab fa-facebook-square" size="2rem"
          />
          <q-icon
            class="cursor-pointer"
            name="fab fa-instagram" size="2rem"
          />
          <q-icon
            class="cursor-pointer"
            name="fab fa-twitter-square" size="2rem"
          />
        </div>
      </div>
    </div>

    <q-dialog v-model="icon">
      <q-card >
        <LogIn @close="icon = false" />
      </q-card>
    </q-dialog>
  </q-layout>
</template>

<script>
import LogIn from '../components/Login'

export default {
  name: 'MyLayout',
  components: {
    LogIn
  },
  data () {
    return {
      leftDrawerOpen: false,
      icon: false
    }
  },
  methods: {
    goHome: function () {
      this.$router.push({ name: 'rootHome' }).catch(() => {})
    }
  }
}
</script>

<style lang="stylus">

</style>
