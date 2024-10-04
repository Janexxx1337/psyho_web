<!-- src/components/ui/UiInput.vue -->
<template>
<el-input
:type="type"
:placeholder="placeholder"
:rows="rows"
:disabled="disabled"
:clearable="clearable"
:size="size"
:class="['ui-input', className]"
v-model="internalValue"
@input="$emit('update:modelValue', internalValue)"
@focus="$emit('focus', $event)"
@blur="$emit('blur', $event)"
:autosize="isTextarea ? { minRows: rows, maxRows: rows } : false"
>
<template v-if="icon" #prefix>
<span class="material-symbols-outlined ui-input__icon">
{{ icon }}
</span>
</template>
<slot />
</el-input>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, ref, watch, computed } from 'vue';

const props = defineProps({
type: {
type: String,
default: 'text', // Тип ввода по умолчанию
},
placeholder: {
type: String,
default: '',
},
modelValue: {
type: [String, Number],
default: '',
},
rows: {
type: Number,
default: 3,
},
disabled: {
type: Boolean,
default: false,
},
clearable: {
type: Boolean,
default: false,
},
icon: {
type: String,
default: '', // Имя иконки (например, 'edit', 'search' и т.д.)
},
size: {
type: String,
default: 'medium', // Размер поля: 'small', 'medium', 'large'
},
className: {
type: String,
default: '',
},
});

const emit = defineEmits(['update:modelValue', 'input', 'focus', 'blur']);

const internalValue = ref(props.modelValue);

watch(
() => props.modelValue,
(newVal) => {
internalValue.value = newVal;
}
);

const isTextarea = computed(() => props.type === 'textarea');
</script>

<style scoped>
.ui-input {
display: flex;
align-items: center;
}

.ui-input__icon {
font-size: 1.2em;
}
</style>
