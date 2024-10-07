<template>
	<div v-if="entries.length" class="chart-section">
		<h3>Динамика настроения</h3>
		<ChartFilters @filter="applyFilter" />
		<VueECharts
			ref="moodChart"
			:option="chartOption"
			autoresize
			class="mood-chart"
		/>
	</div>
</template>

<script setup lang="ts">
	import { ref, watch, computed } from 'vue';
	import VueECharts from 'vue-echarts';
	import { use } from 'echarts/core';
	import { LineChart } from 'echarts/charts';
	import { CanvasRenderer } from 'echarts/renderers';
	import {
		GridComponent,
		TooltipComponent,
		TitleComponent,
		LegendComponent,
	} from 'echarts/components';
	import ChartFilters from './ChartFilters.vue';

	// Регистрируем необходимые компоненты echarts
	use([
		CanvasRenderer,
		LineChart,
		GridComponent,
		TooltipComponent,
		TitleComponent,
		LegendComponent,
	]);

	const props = defineProps({
		entries: {
			type: Array,
			required: true,
		},
	});

	const chartOption = ref({});

	const filter = ref('all');

	const applyFilter = (period) => {
		filter.value = period;
	};

	const filteredEntries = computed(() => {
		let filtered = [...props.entries];
		const now = new Date();

		if (filter.value === 'week') {
			const weekAgo = new Date();
			weekAgo.setDate(now.getDate() - 7);
			filtered = filtered.filter((entry) => new Date(entry.date) >= weekAgo);
		} else if (filter.value === 'month') {
			const monthAgo = new Date();
			monthAgo.setMonth(now.getMonth() - 1);
			filtered = filtered.filter((entry) => new Date(entry.date) >= monthAgo);
		}
		return filtered;
	});

	const updateChart = () => {
		const dates = filteredEntries.value.map((entry) => entry.date);
		const ratings = filteredEntries.value.map((entry) => entry.rating);

		chartOption.value = {
			xAxis: {
				type: 'category',
				data: dates,
			},
			yAxis: {
				type: 'value',
				min: 0,
				max: 10,
			},
			series: [
				{
					data: ratings,
					type: 'line',
					smooth: true,
					areaStyle: {
						color: 'rgba(115, 183, 245, 0.2)',
					},
					lineStyle: {
						width: 3,
						color: '#73b7f5',
					},
					itemStyle: {
						borderWidth: 2,
						color: '#409EFF',
					},
				},
			],
			tooltip: {
				trigger: 'axis',
			},
			grid: {
				left: '3%',
				right: '4%',
				bottom: '3%',
				containLabel: true,
			},
		};
	};

	watch(filteredEntries, updateChart, { immediate: true });
</script>

<style scoped>
	.mood-chart {
		width: 100%;
		height: 200px;
	}
</style>
