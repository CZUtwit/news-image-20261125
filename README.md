# The World in One Day — 25 November 2026

Entry for the make.fun competition `news-image-20261125`: a program that
writes a single image summarising the world news of Wednesday 25 November
2026 to `/output/entry.png`.

## How it works

`main.ts` (Node 22, standard library only) copies the pre-rendered
`entry.png` from the repository root to `/output/entry.png`.

`entry.png` itself is generated locally by `tools/make_image.py` (pure
Pillow, no network): a champion-format broadsheet with 13 main stories,
14 more in ALSO TODAY, region chips, a UTC timeline, a dotted world map
with pins, a DATE CHECK listing stories first reported on earlier days,
and a HOW SURE legend. Running the generator twice produces byte-identical
output (sha256 verified).

## Contents

- 27 stories, all first reported on 25 November 2026 (UTC), each verified
  against wire or official sources before inclusion.
- 13 main stories with place, category, headline, summary, source and a
  REPORTED / CLAIM status badge; 14 further stories in ALSO TODAY.
- DATE CHECK: 12 stories deliberately excluded because they were first
  reported on Tuesday 24 November (Huawei verdict, Chen Jining probe,
  Tidal AI-music ban, Broadcom VMware flaws, UNAIDS HIV report, Democrats'
  259 House seats, Giuliani Medal of Freedom, Xiamen Boeing order,
  Cameroon separatist trial, SpaceX USSF-266, Canada Para hockey 10–0,
  Abrego Garcia departure).

## Reproduce

```sh
python3 tools/make_image.py   # writes entry.png (1024x1024, <1 MiB)
```

## License

MIT — see `LICENSE`.
