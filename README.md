# Onde o Dinheiro Cai · vídeo de apresentação

Vídeo de 1min22 (1080×1350, 4:5, feed do LinkedIn) sobre a pesquisa [ondeodinheirocai.com.br](https://ondeodinheirocai.com.br): emendas Pix (EC 105/2019) cruzadas com o Censo 2022.
Feito em [HyperFrames](https://github.com/heygen-com/hyperframes): cada cena é HTML + GSAP, e o mapa da cena 2 é three.js com os 5.499 municípios reais.

## O que tem aqui

| Arquivo | Para que serve |
| --- | --- |
| `index.html` | A composição inteira (7 cenas, mapa 3D, efeitos sonoros) |
| `SCRIPT.md` | Texto da narração por cena + textos para gravar as amostras da voz |
| `BRIEF.md`, `frame.md` | Briefing e identidade visual (cores do site) |
| `ledger.json` | Plano das transições entre cenas (motion-doctrine do HyperFrames) |
| `audio_meta.json` | Lista dos 52 efeitos sonoros com tempo e volume |
| `assets/js/` | GSAP, three.js, dados do mapa (`mapdata.js`) e divisas dos estados (`ufdata.js`) |
| `assets/sfx/` | Efeitos sonoros minimalistas, gerados por `make_sfx.py` |
| `assets/voz/` | Onde entram os WAVs da narração (`cena-1.wav` a `cena-7.wav`) |
| `tools/` | `seam-stamp.mjs` e `seam-gate.mjs` para regenerar e verificar as transições |

Os vídeos renderizados (`renders/`) ficam fora do Git. Gere de novo com `npm run render`.

## Rodar no Mac

Precisa de Node 22+ e ffmpeg (`brew install node ffmpeg`).

```bash
npx hyperframes@0.8.141 preview      # abre o Studio para ver e editar
npx hyperframes@0.8.141 check        # valida layout, contraste e animações
npx hyperframes@0.8.141 render --quality high --output renders/video.mp4
```

## Narração com a sua voz (Voicebox no Mac)

1. Instale o Voicebox para Mac (Apple Silicon usa MLX, bem mais rápido): voicebox.sh/download/mac-arm
2. Grave 2 ou 3 amostras de 15 a 30 s (textos prontos no fim do `SCRIPT.md`), em lugar silencioso.
3. Profiles → New Profile → Qwen3-TTS → suba as amostras com o texto lido em cada uma.
4. Gere as 7 falas do `SCRIPT.md` em Português, mesma seed, e salve como `assets/voz/cena-1.wav` … `cena-7.wav`.
5. Faça commit e push dos WAVs (ou peça ao Claude no Mac para fazer o passo abaixo).

### Prompt para continuar no Claude Code (Mac)

> Leia README.md, SCRIPT.md, ledger.json e index.html. Os WAVs da narração estão em assets/voz.
> Encaixe a narração no vídeo: cada cena começa no início do seu WAV e dura até o fim dele mais 0,4 s;
> reposicione as animações internas de cada cena nos trechos de fala correspondentes; atualize os cortes
> em ledger.json, rode `node tools/seam-stamp.mjs --ledger ledger.json --write index.html` e verifique com
> `tools/seam-gate.mjs`. Baixe os efeitos sonoros uns 6 dB enquanto a voz fala e normalize a mistura em
> -14 LUFS. Rode `npx hyperframes@0.8.141 check` e só renderize depois de eu aprovar.

## Créditos e licenças

- Dados: Transferegov (EC 105/2019), IBGE Censo 2022, malha municipal do IBGE, via ondeodinheirocai.com.br.
- three.js (MIT), GSAP (licença padrão gratuita da GreenSock), fontes Inter e JetBrains Mono (SIL OFL).
- `tools/seam-*.mjs` vêm do repositório HyperFrames (Apache 2.0).
- Efeitos sonoros sintetizados para este projeto.
- A narração será gerada por IA a partir da voz do autor; vale indicar isso ao publicar.
