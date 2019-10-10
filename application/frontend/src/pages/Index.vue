<template>
  <q-page class="q-pa-sm">
    <div
      class="shadow-2 q-pa-md" align="center"
      style="
        margin: 1em auto;
        max-width: 98%;
        border-radius: 3px;
      "
    >
      <strong>
        Since we are still in Milestone 0, nothing has been pushed for the home page. That being said, please checkout our about page by clicking on <router-link :to="'/about'">'About Us'</router-link> or the 'About' tab from our side menu.
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
            <MockTable />
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
