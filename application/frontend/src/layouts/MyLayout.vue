<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat dense round
          aria-label="Menu"
          @click="leftDrawerOpen = !leftDrawerOpen"
        >
          <q-icon name="menu" />
        </q-btn>

        <q-toolbar-title class="absolute-center">
          DIYup
        </q-toolbar-title>

        <q-space />
        <q-btn flat no-caps label="Log In" @click="icon = true" />
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      content-class="bg-grey-2"
    >
      <q-list>
        <q-item-label header>Navigation</q-item-label>
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

    <q-page-container>
      <router-view />
    </q-page-container>

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
  }
}
</script>

<style lang="stylus">

</style>
