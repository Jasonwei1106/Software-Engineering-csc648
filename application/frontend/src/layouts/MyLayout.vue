<template>
  <q-layout view="hHh lpR fFf">
    <q-header reveal elevated class="bg-primary text-white">
      <q-toolbar>
        <q-space />

        <div
          class="cursor-pointer" style="width: 80px;"
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
                <q-btn
                  dense round
                  size="md"
                  @click="leftDrawerOpen = !leftDrawerOpen"
                >
                  <q-avatar size="md" text-color="white" icon="person" />
                </q-btn>
              </div>

              <q-separator dark vertical />

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
              v-model="filter" placeholder = "Tutorial Title"
              @keyup.enter="titleSearch"
            >
              <template v-slot:append>
                <q-icon v-if="filter === ''" name="search" />
                <q-icon
                  v-else
                  name="clear" class="cursor-pointer"
                  @click="refreshSearch"
                />
              </template>
            </q-input>
          </div>
        </div>
      </q-toolbar>

      <q-toolbar
        v-if="$route.name && $route.name === 'rootHome' && !leftDrawerOpen"
        class="bg-white text-black"
      >
        <q-toolbar-title class="row q-pa-md">
          <div class="col" align="center" >
            <strong
              class="gt-sm"
              style="
                font-size: 1.5em;
                position: relative;
                top: 15%;
                transform: translateY(-50%);
              "
            >
              STEP-BY-STEP PROJECTS BY USERS FOR USERS
            </strong>

            <strong
              class="sm"
              style="
                font-size: 1em;
                position: relative;
                top: 20%;
                transform: translateY(-50%);
              "
            >
              STEP-BY-STEP PROJECTS BY USERS FOR USERS
            </strong>

            <strong class="lt-sm" style="font-size: .6em;">
              STEP-BY-STEP PROJECTS BY USERS FOR USERS
            </strong>
          </div>

          <img
            class="col-2 q-mr-md gt-xs"
            src="../statics/icons/DIY_Artwork.png"
            style="width: 10%; max-width: 100px; max-height: 70px;"
          />
        </q-toolbar-title>
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

        <q-item to="/" exact>
          <q-item-section avatar>
            <q-icon name="list" />
          </q-item-section>

          <q-item-section>
            <q-item-label>Home</q-item-label>
          </q-item-section>
        </q-item>

        <q-item
          :to="`/tutorials/${$q.localStorage.getItem('__diyup__username')}`"
          exact
        >
          <q-item-section avatar>
            <q-icon name="where_to_vote" />
          </q-item-section>

          <q-item-section>
            <q-item-label>My Tutorials</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container style="min-height: 90vh;">
      <router-view />
    </q-page-container>

    <div style="background-color: #027BE3; height: 100px;" >
      <div class="row" style="width: 96%; margin: 0 auto;">
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
  created () {
  },
  updated () {
  },
  data () {
    return {
      leftDrawerOpen: false,
      icon: false,
      filter: ''
    }
  },
  methods: {
    refreshSearch: function () {
      this.filter = ''
      this.titleSearch(event)
    },
    titleSearch: function (e) {
      if (e.target.value) {
        this.$router.push(`/?title=${e.target.value}`).catch(err => {
          if (err) {
            // error
          }
        })
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
      this.$q.localStorage.remove('__diyup__username')

      if (this.$route.name === 'rootHome') {
        this.$router.go()
      } else {
        this.$router.push({ name: 'rootHome' }).catch(err => {
          if (err) {
            // error
          }
        })
      }
    }
  }
}
</script>

<style lang="stylus">

</style>
