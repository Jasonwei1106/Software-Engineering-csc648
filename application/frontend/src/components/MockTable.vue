<template>
  <div class="">
      <!-- title="DIYup Tutorials" -->
    <q-table
      flat hide-header wrap-cells
      separator="none"
      row-key="title"
      :data="curData"
      :columns="columns"
      :filter="option.value"
      :pagination.sync="pagination"
    >
      <template v-slot:top-left>
        <q-btn
          outline
          label="Create a new project"
          @click="goToPost"
          v-if="$q.localStorage.has('__diyup__signedIn')"
        />
      </template>

      <template v-slot:top-right>
        <q-toolbar>
          <q-select
            outlined dense
            class="q-mr-xs col-4" label="Category Filter"
            bg-color="white" color="black"
            v-model="option"
            style="width: 150px;"
            :options="categories"
          />
        </q-toolbar>
      </template>

      <!-- <template v-slot:body-cell-title="props">
        <q-td :props="props">
          <div>
            <q-badge color="purple" :label="props.value" />
          </div>
        </q-td>
      </template> -->

      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td colspan="100%" key="title" :props="props">
            <q-card class="q-pa-md" style="min-height: 15vh;">
              <div class="row cursor-pointer" @click="routeToTutorial(props.row)">
                <div class="col-4" align="center">
                  <q-img
                    :src="'https://placeimg.com/500/300/nature?t=' + Math.random()"
                    spinner-color="primary"
                    style="height: 140px; max-width: 150px"
                  />
                </div>
                <div class="col">
                  <b>Title:</b>
                  {{ props.row.title }} by {{ props.row.author_id }}<br>

                  <b>Author's Difficulty Rating:</b>
                  {{ props.row.author_difficulty }}<br>

                  <b>Users' Difficulty Rating:</b>
                  {{ props.viewer_difficulty }}<br>

                  <b>Users' Rating:</b>
                  {{ props.row.rating }}<br>

                  <b>Category:</b>
                  {{ props.row.category }}<br>
                </div>

                <div class="col-5 q-pr-xl" align="left">
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                </div>
              </div>
            </q-card>
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  // props: {
  //   filter: String
  // },
  watch: {
    $route: 'titleQueryFilter'
  },
  created () {
    this.fetchData()
    this.filter = this.$route.query.title || ''
  },
  data () {
    return {
      filter: '',
      categories: [
        { label: 'Electronics', value: 'electronics' },
        { label: 'Coding', value: 'coding' },
        { label: 'Robotics', value: 'robotics' },
        { label: 'Cooking', value: 'cooking' },
        { label: 'Crafts', value: 'crafts' },
        { label: 'Home & Decor', value: 'homeDecor' },
        { label: 'Testing', value: 'testing' },
        { label: 'All', value: '' }
      ],
      option: '',
      columns: [
        {
          name: 'title',
          label: 'Title',
          required: true,
          align: 'left',
          field: row => row.title,
          format: val => `${val}`,
          sortable: true
        },
        {
          name: 'author_difficulty',
          label: `Creator's Difficulty`,
          required: true,
          align: 'left',
          field: row => row.author_difficulty,
          format: val => `${val}`,
          sortable: true
        },
        {
          name: 'category',
          label: `Category`,
          required: true,
          align: 'left',
          field: row => row.category,
          format: val => `${val}`,
          sortable: true
        }
      ],
      data: [],
      curData: [],
      pagination: {
        rowsPerPage: 10,
        sortBy: 'name',
        descending: false
      }
    }
  },
  methods: {
    routeToTutorial: function (entry) {
      this.$router.push(`/tutorial/${entry.uuid}`)
    },
    titleQueryFilter: function () {
      this.filter = this.$route.query.title
      if (this.filter) {
        this.curData = this.data.filter(v => v.title.toLowerCase().includes(this.filter.toLowerCase()))
      } else {
        this.curData = this.data
      }
    },
    fetchData: function () {
      axios.get('http://54.153.68.76:5000/api/tutorial/get')
        .then(res => {
          this.data = res.data.tutorials
          this.data.forEach(element => {
            this.curData.push(element)
          })

          // console.log(this.data)
        })
    },
    goToPost: function () {
      if (this.$q.localStorage.has('__diyup__signedIn')) {
        this.$router.push({ path: '/post' }).catch(err => {
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
.my-table-details {
  font-size: 0.85em;
  font-style: italic;
  max-width: 200px;
  white-space: normal;
  color: #555;
  margin-top: 4px;
}
</style>
