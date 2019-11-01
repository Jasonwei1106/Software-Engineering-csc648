<template>
  <q-layout view="hHh lpR fFf">
    <q-header reveal elevated class="bg-primary text-white">
      <q-toolbar>
        <div style="min-width: 40px;" >
          <q-btn
            :hidden="leftDrawerOpen"
            flat dense round
            aria-label="Menu"
            @click="leftDrawerOpen = !leftDrawerOpen"
            icon="arrow_right"
          />
        </div>

        <q-space />

        <div
          class="cursor-pointer"
          style="width: 80px;"
          @click="routeTo('rootHome')"
        >
          <q-img src="../statics/icons/96p.png" />
        </div>

        <q-space />

        <div
          class="q-my-xs" align="center"
          style="max-width: 51vw;"
        >
          <div v-if="!$q.localStorage.has('__diyup__signedIn')">
            <div class="row">
              <div class="col">
                <q-btn
                  flat no-caps
                  label="Log In" class="full-width"
                  @click="icon = true"
                />
              </div>

              <q-separator dark vertical />

              <div class="col">
                <q-btn
                  flat no-caps
                  label="Sign Up" class="full-width"
                  to="/register"
                />
              </div>
            </div>
          </div>

          <div v-else>
            <div class="row">
              <div class="col">
                <q-avatar color="red" text-color="white" icon="directions" />
              </div>

              <!-- <q-separator dark vertical /> -->

              <div class="col">
                <q-btn
                  flat no-caps
                  label="Log Out" class="full-width"
                  @click="logout"
                />
              </div>
            </div>
          </div>

          <div class="row q-mt-xs">
            <q-input
              borderless dense outlined
              bg-color="white" color="black"
              debounce="300" class="col"
              v-model="filter" placeholder = "Search"
              @keyup.enter="test"
            >
              <template v-slot:append>
                <q-icon v-if="filter === ''" name="search" />
                <q-icon
                  v-else
                  name="clear" class="cursor-pointer" @click="filter = ''"
                />
              </template>
            </q-input>
          </div>
        </div>
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
        <div class="text-white cursor-pointer" @click="routeTo('rootAbout')">
          About Us
        </div>
      </div>

      <div class="q-pa-md" align="center">
        <div class="text-white">
          Follow Us On
        </div>

        <div>
          <q-icon
            class="cursor-pointer"
            name="fab fa-facebook-square" size="2rem"
            @click="goTo('https://www.facebook.com')"
          />
          <q-icon
            class="cursor-pointer"
            name="fab fa-instagram" size="2rem"
            @click="goTo('https://www.instagram.com/')"
          />
          <q-icon
            class="cursor-pointer"
            name="fab fa-twitter-square" size="2rem"
            @click="goTo('https://twitter.com/')"
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

// window.addEventListener('beforeunload', function (e) {
//   // Cancel the event
//   e.preventDefault()
//   // Chrome requires returnValue to be set
//   e.returnValue = ''
// })

// window.onbeforeunload = function () {
//   return 'Are you sure you want to close the window?'
// }

export default {
  name: 'MyLayout',
  components: {
    LogIn
  },
  created () {
  },
  data () {
    return {
      leftDrawerOpen: false,
      icon: false,
      filter: ''
    }
  },
  methods: {
    test: function (e) {
      if (e.target.value) {
        this.$router.push(`/?title=${e.target.value}`).catch(err => {
          if (err) {
            // error
          }
        })
        this.filter = ''
      } else {
        this.$router.push('/').catch(err => {
          if (err) {
            // error
          }
        })
      }
    },
    goTo: function (entry) {
      window.location.href = entry
    },
    routeTo: function (entry) {
      this.$router.push({ name: entry }).catch(() => {})
    },
    logout: function () {
      this.$q.localStorage.remove('__diyup__signedIn')
      this.$router.go()
    }
  }
}
</script>

<style lang="stylus">

</style>
