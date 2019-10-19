<template>
  <q-page class="q-pa-sm">
    <div style ="margin-left: 1200px; padding:4px; border: 1px solid grey;">
        <q-input borderless dense debounce="300" color="primary" v-model="filter" placeholder = "search">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
    </div>
    <div
      class="shadow-2 q-pa-md" align="center"
      style="
        margin: 1em auto;
        max-width: 98%;
        border-radius: 3px;
      "
    >
      <strong>
        Please checkout our about page by clicking on <router-link :to="'/about'">'About Us'</router-link> or the 'About' tab from our side menu.
      </strong>
    </div>
    <hr>
    <div class="q-pa-md">
      <q-card>
        <q-tabs
          inline-label
          align="justify"
          class="bg-purple text-white shadow-2"
          v-model="pageTab"
          :breakpoint="0"
        >
          <q-route-tab exact name="hot" label="What's Hot?" to="/hot" no-caps />
          <q-route-tab exact name="new" label="What's New?" to="/new" no-caps />
          <!-- <q-tab v-if="$q.screen.gt.sm" name="movies" label="Movies" />
          <q-tab v-if="$q.screen.gt.sm" name="photos" label="Photos" />
          <q-btn-dropdown v-if="$q.screen.lt.md" auto-close stretch flat label="More...">
            <q-list link>
              <q-item clickable @click="tab = 'movies'">
                <q-item-section>Movies</q-item-section>
              </q-item>

              <q-item clickable @click="tab = 'photos'">
                <q-item-section>Photos</q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown> -->
        </q-tabs>

        <q-separator />

        <q-tab-panels v-model="pageTab" animated>
          <q-tab-panel name="hot">
            <div class="text-h6">What's Hot</div>
            <MockTable :filter = this.filter />
          </q-tab-panel>

          <q-tab-panel name="new">
            <div class="text-h6">What's New</div>
            <MockTable />
          </q-tab-panel>
        </q-tab-panels>
      </q-card>
    </div>
  </q-page>
</template>

<script>
import MockTable from '../components/MockTable'

export default {
  name: 'PageIndex',
  components: {
    MockTable
  },
  created () {
    this.setPageTab()
  },
  beforeUpdate () {
    this.setPageTab()
  },
  data () {
    return {
      filter: '',
      pageTab: ''
    }
  },
  methods: {
    setPageTab: function () {
      if (this.$route.path === '/') {
        this.pageTab = 'hot'
      }
    }
  }
}
</script>

<style lang="stylus">

</style>
