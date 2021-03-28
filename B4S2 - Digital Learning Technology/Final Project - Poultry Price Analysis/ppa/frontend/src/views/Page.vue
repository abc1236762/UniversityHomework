<template>
  <div class="page">
    <v-card class="ma-4 mx-sm-auto" raised max-width="600px">
      <v-list-item>
        <v-list-item-content>
          <v-icon class="icon" large v-text="item.icon"></v-icon>
        </v-list-item-content>
      </v-list-item>
      <v-list-item two-line>
        <v-list-item-content>
          <v-list-item-title class="headline text-center" v-text="item.title" />
          <v-list-item-subtitle class="text-center">
            更新時間：{{ data[0].date }}
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-list-item>
        <v-row align="center">
          <v-col />
          <v-col class="display-3" cols="auto" v-text="price" />
          <v-col>
            <v-row>
              <v-icon large :color="trend.color" v-text="trend.icon" />
            </v-row>
            <v-row v-text="dataUnit" />
          </v-col>
        </v-row>
      </v-list-item>
    </v-card>
    <v-card class="ma-4 mx-sm-auto" raised max-width="600px">
      <v-card-title>歷史資料</v-card-title>
      <div class="pa-4">
        <v-dialog
          ref="datePickerDialog"
          v-model="isDatePickerEnabled"
          :return-value.sync="dateRange"
          persistent
          width="290px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="dateRangeText"
              label="選擇日期範圍"
              prepend-icon="mdi-calendar-range"
              readonly
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker
            v-model="dateRange"
            scrollable
            range
            show-current="false"
            :min="dateRangeMin"
            :max="dateRangeMax"
            :allowed-dates="allowedDates"
            :title-date-format="titleDateFormat"
            :selected-items-text="dateRangeText"
            :day-format="dayFormat"
          >
            <v-spacer />
            <v-btn text color="primary" @click="isDatePickerEnabled = false">
              取消
            </v-btn>
            <v-btn
              text
              color="primary"
              @click="$refs.datePickerDialog.save(dateRange)"
            >
              確定
            </v-btn>
          </v-date-picker>
        </v-dialog>
      </div>
      <line-chart
        class="pa-4"
        v-if="isLineChartLoaded"
        :chart-data="lineChartData"
        :options="{ legend: { display: false } }"
      />
      <v-data-table
        :headers="dataTableHeaders"
        :items="dataTableItems"
        :loading="isDataTableLoading"
        dense
        mobile-breakpoint=""
      />
    </v-card>
    <v-card class="ma-4 mx-sm-auto" raised max-width="600px">
      <v-card-title>未來預測</v-card-title>
      <div class="pa-4">
        <v-form ref="predForm" v-model="isPredFormValid">
          <v-row>
            <v-col>
              <v-text-field
                v-model="pastText"
                :rules="intRules"
                label="從最近"
                suffix="天"
                type="number"
                required
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                v-model="futureText"
                :rules="intRules"
                label="預測後"
                suffix="天"
                type="number"
                required
              ></v-text-field>
            </v-col>
          </v-row>
          <v-btn
            block
            color="success"
            @click="predict"
            :disabled="!isPredFormValid"
          >
            預測
          </v-btn>
        </v-form>
      </div>
      <div id="pred">
        <line-chart
          class="pa-4"
          v-if="isPredLineChartLoaded"
          :chart-data="predLineChartData"
          :options="{ legend: { display: false } }"
        />
      </div>
      <v-overlay :value="isPredicting" absolute>
        <v-progress-circular indeterminate size="64" />
      </v-overlay>
    </v-card>
    <v-snackbar v-model="predFailedSnackbar">
      <div class="text-center">天數超出資料數量，無法預測</div>
      <template v-slot:action="{ attrs }">
        <v-btn
          color="info"
          text
          v-bind="attrs"
          @click="predFailedSnackbar = false"
        >
          關閉
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<style lang="scss">
.icon {
  color: black;
  font-style: normal;
}
// 輸入數字的框內數字要靠右
input[type='number'] {
  text-align: right;
}
</style>

<script>
import { getValueString } from '@/utils';
import data, { dataItems, dataUnit, getPrediction } from '@/services/data';

import Vue from 'vue';
import Chart from 'chart.js';
import { Line, mixins } from 'vue-chartjs';

Chart.defaults.global.defaultFontFamily =
  '"Noto Sans", "Noto Sans TC", "Noto Color Emoji", sans-serif';
// 建立折線圖元件
const LineChart = Vue.component('line-chart', {
  extends: Line,
  mixins: [mixins.reactiveProp],
  props: {
    options: {
      type: Object,
      default: null,
    },
  },
  mounted() {
    this.renderChart(this.chartData, this.options);
  },
});

export default {
  components: { LineChart },
  data: () => ({
    isDatePickerEnabled: false,
    isDataTableLoading: true,
    dataUnit: dataUnit,
    dateRange: [],
    dataTableHeaders: [
      {
        text: '日期',
        value: 'date',
        align: 'center',
        sortable: false,
      },
      { text: `價格（${dataUnit}）`, value: 'value', align: 'end' },
    ],
    dataTableItems: [],
    isLineChartLoaded: false,
    lineChartData: {},
    intRules: [(v) => /^[1-9]\d*$/.test(v) || '必須是大於0的整數'],
    isPredFormValid: true,
    isPredicting: false,
    pastText: 60,
    futureText: 10,
    isPredLineChartLoaded: false,
    predLineChartData: {},
    predFailedSnackbar: false,
  }),
  computed: {
    item() {
      for (const dataItem of dataItems) {
        if (dataItem.key === this.$route.params.key) return dataItem;
      }
      return null;
    },
    data() {
      return data.get(this.item.title);
    },
    price() {
      return getValueString(this.data[0].value);
    },
    trend() {
      const trend = {};
      const diff = this.data[0].value - this.data[1].value;
      trend.icon = 'mdi-trending-neutral';
      if (diff > 0) {
        trend.color = 'red';
        trend.icon = 'mdi-trending-up';
      } else if (diff < 0) {
        trend.color = 'green';
        trend.icon = 'mdi-trending-down';
      }
      return trend;
    },
    dates() {
      return this.data.map((d) => d.date).sort();
    },
    dateRangeMin() {
      return this.dateOfIndex(this.dates.length - 1);
    },
    dateRangeMax() {
      return this.dateOfIndex(0);
    },
    dateRangeText() {
      return this.titleDateFormat(this.dateRange);
    },
  },
  methods: {
    dateOfIndex(index) {
      return this.dates[this.dates.length - 1 - index].split('/').join('-');
    },
    allowedDates(date) {
      return this.dates.includes(date.split('-').join('/'));
    },
    dayFormat(date) {
      return date.split('-')[2].toString();
    },
    titleDateFormat(date) {
      return date
        .map((dt) => dt.replace(/(\d{4})-(\d{2})-(\d{2})/, '$1年$2月$3日'))
        .sort()
        .join('～');
    },
    // 設置資料表格內的內容以及折線圖
    setDataTableItems() {
      let begin = this.dates.indexOf(this.dateRange[0].split('-').join('/'));
      let end = this.dates.indexOf(
        this.dateRange[this.dateRange.length - 1].split('-').join('/')
      );
      if (begin > end) [begin, end] = [end, begin];
      const dates = this.dates.slice(begin, end + 1);
      // 設置資料表格的內容
      this.dataTableItems = this.data
        .filter((d) => dates.includes(d.date.split('-').join('/')))
        .map((d) => ({
          date: d.date.replace(/(\d{4})\/(\d{2})\/(\d{2})/, '$1年$2月$3日'),
          value: getValueString(d.value),
        }));
      // 設置折線圖的內容
      this.lineChartData = {
        labels: this.dataTableItems
          .map((d) =>
            d.date.replace(/20(\d{2})年(\d{2})月(\d{2})日/, '’$1/$2/$3')
          )
          .reverse(),
        datasets: [
          {
            label: '價格',
            borderColor: '#FFD600',
            borderWidth: 2.5,
            backgroundColor: '#FFEB3B',
            pointHoverRadius: 3,
            pointRadius: 2,
            fill: false,
            data: this.dataTableItems.map((d) => Number(d.value)).reverse(),
          },
        ],
      };
    },
    // 進行預測並且顯示預測折線圖
    async predict() {
      const past = Number(this.pastText);
      const future = Number(this.futureText);
      if (!Number.isInteger(past) || !Number.isInteger(future)) return;
      this.isPredLineChartLoaded = false;
      this.isPredicting = true;
      const result = await getPrediction(this.item.title, past, future);
      if (!result) {
        // 沒有結果的話一定是天數超出範圍
        this.isPredicting = false;
        this.predFailedSnackbar = true;
        return;
      }
      const xs = Array.from(Array(past + future).keys()).map(
        (i) => i - past + 1
      );
      // 設置預測折線圖的內容
      this.predLineChartData = {
        labels: xs.map((x) => {
          if (x > 0) return `後${x}天`;
          else if (x < 0) return `前${Math.abs(x)}天`;
          else return '今天';
        }),
        datasets: [
          {
            label: '真實',
            borderColor: '#FFD600',
            backgroundColor: '#FFEB3B',
            pointHoverRadius: 2,
            pointRadius: 1,
            fill: false,
            showLine: false,
            data: xs.slice(0, past).map((x) => result[x + past - 1]),
          },
          {
            label: '過去預測',
            borderColor: '#00BFA5',
            borderWidth: 1.5,
            borderDash: [4, 1],
            backgroundColor: '#009688',
            pointHoverRadius: 2,
            pointRadius: 1,
            fill: false,
            data: xs.slice(0, past).map((x) => result[x + past * 2 - 1]),
          },
          {
            label: '未來預測',
            borderColor: '#DD2C00',
            borderWidth: 2.5,
            backgroundColor: '#FF5722',
            pointHoverRadius: 3,
            pointRadius: 2,
            fill: false,
            data: xs.map((x) => (x > 0 ? result[x + past * 2 - 1] : null)),
          },
        ],
      };
      this.isPredLineChartLoaded = true;
      this.isPredicting = false;
    },
  },
  created() {
    this.dateRange = [this.dateOfIndex(59), this.dateOfIndex(0)];
  },
  watch: {
    // 當資料範圍變更時重新設置表格等
    dateRange() {
      this.isDataTableLoading = true;
      this.isLineChartLoaded = false;
      this.setDataTableItems();
      this.isDataTableLoading = false;
      this.isLineChartLoaded = true;
    },
  },
};
</script>
