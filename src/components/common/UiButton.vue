<!-- src/components/ui/UiButton.vue -->
<template>
	<el-button
		:type="type"
		:native-type="nativeType"
		:size="size"
		:disabled="disabled"
		:loading="loading"
		:class="['ui-button', className]"
		@click="$emit('click', $event)"
	>
		<span v-if="icon" class="material-symbols-outlined ui-button__icon">
			{{ icon }}
		</span>
		<slot />
	</el-button>
</template>

<script setup lang="ts">
	import { defineProps, defineEmits } from 'vue';

	const props = defineProps({
		type: {
			type: String,
			default: 'primary', // Тип кнопки по умолчанию
		},
		nativeType: {
			type: String,
			default: 'button', // Тип HTML кнопки по умолчанию
		},
		icon: {
			type: String,
			default: '', // Имя иконки (например, 'edit', 'save' и т.д.)
		},
		size: {
			type: String,
			default: 'medium', // Размер кнопки: 'small', 'medium', 'large'
		},
		disabled: {
			type: Boolean,
			default: false, // Отключение кнопки
		},
		loading: {
			type: Boolean,
			default: false, // Состояние загрузки
		},
		className: {
			type: String,
			default: '', // Дополнительные классы для стилизации
		},
	});

	const emit = defineEmits(['click']);
</script>

<style scoped>
	.ui-button {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.ui-button__icon {
		font-size: 1.2em;
	}
</style>
