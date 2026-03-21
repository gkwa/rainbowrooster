# rainbowrooster

Generates markdown product files for an Obsidian vault, with frontmatter fields and
section headers for each store. Also generates Obsidian Base configuration files for
shopping list views.

Store list is sourced from buf.build/gkwa/heatedhornet (see github.com/gkwa/heatedhornet).

## installation

```bash
pipx install rainbowrooster
```

## usage

```bash
rainbowrooster --products myproducts.txt --outdir '/Users/mtm/Documents/Obsidian Vault'
rainbowrooster --products myproducts.txt --outdir '/Users/mtm/Documents/Obsidian Vault' -v
rainbowrooster --annotate-test --products myproducts.txt --outdir .
rainbowrooster --version
```

## updating the store list

The store list comes from generated protobuf stubs in src/rainbowrooster/gen/. When
heatedhornet adds a new store:

1. buf generate (from this directory)
2. git commit the regenerated stores_pb2.py
3. pipx reinstall rainbowrooster
