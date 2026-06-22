const fs = require('fs');
const path = require('path');
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

const ajv = new Ajv({ allErrors: true });
addFormats(ajv);

const args = process.argv.slice(2);
const typeIndex = args.indexOf('--type');
const type = typeIndex !== -1 ? args[typeIndex + 1] : null;

if (type === 'schemas') {
  const schemaDir = path.join(__dirname, '../agents/schemas');
  const files = fs.readdirSync(schemaDir);
  let success = true;

  files.forEach(file => {
    try {
      const schema = JSON.parse(fs.readFileSync(path.join(schemaDir, file), 'utf8'));
      ajv.compile(schema);
      console.log(`✓ Schema valid: ${file}`);
    } catch (e) {
      console.error(`✗ Schema invalid: ${file}`, e.message);
      success = false;
    }
  });

  process.exit(success ? 0 : 1);
} else if (type === 'handoff') {
  const handoffPath = args[args.indexOf('--file') + 1];
  const schemaName = args[args.indexOf('--schema') + 1];

  if (!handoffPath || !schemaName) {
    console.error('Usage: node scripts/validate.js --type handoff --file <path> --schema <name>');
    process.exit(1);
  }

  try {
    const handoff = JSON.parse(fs.readFileSync(handoffPath, 'utf8'));
    const schema = JSON.parse(fs.readFileSync(path.join(__dirname, '../agents/schemas', schemaName), 'utf8'));

    const validate = ajv.compile(schema);
    const valid = validate(handoff);

    if (valid) {
      console.log(`✓ Handoff valid: ${handoffPath}`);
      process.exit(0);
    } else {
      console.error(`✗ Handoff invalid: ${handoffPath}`, validate.errors);
      process.exit(1);
    }
  } catch (e) {
    console.error('Validation error:', e.message);
    process.exit(1);
  }
} else {
  console.log('Validation type not implemented or recognized.');
  process.exit(0);
}
