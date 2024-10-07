<template>
	<div class="mood-icon">
		<span>{{ emoji }}</span>
	</div>
</template>

<script setup lang="ts">
	import { computed } from 'vue';
	interface Props {
		rating: number;
	}
	const props = defineProps<Props>();

	const emoji = computed(() => {
		const rating = props.rating;
		if (rating <= 2) return '😢';
		else if (rating <= 4) return '😟';
		else if (rating <= 6) return '😐';
		else if (rating <= 8) return '😊';
		else return '😄';
	});
</script>

<style scoped>
	.mood-icon {
		font-size: 24px;
	}

	.mood-icon-large {
		font-size: 48px;
	}
</style>
