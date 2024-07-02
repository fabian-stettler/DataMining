const fs = require('fs');
const readline = require('readline');

const filePath = 'C:\Users\fabia\Documents\Coding_Projekte\DataMining\src\main\control.js';

const rl = readline.createInterface({
	input: fs.createReadStream(filePath),
	output: process.stdout,
	terminal: false
});

const dependencies = new Set();

rl.on('line', (line) => {
	const requireMatch = line.match(/require\(['"`](.*?)['"`]\)/);
	const importMatch = line.match(/import .* from ['"`](.*?)['"`]/);

	if (requireMatch) {
		dependencies.add(requireMatch[1]);
	}

	if (importMatch) {
		dependencies.add(importMatch[1]);
	}
});

rl.on('close', () => {
	console.log('Dependencies:', Array.from(dependencies));
});
