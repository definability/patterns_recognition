# Recognize noisy string with letters

This app draws and recognizes string with capital letters.

Example of use:
```bash
python -m examples.dynamic_programming.letters_string 1000 A .1 B .1 C .1 D .1 E .1 F .1
```
where
- `1000` is a number of letters;
- `A`, `B`, `C`, `D`, `E`, `F` are letters;
- `.1` are probabilities of each letter.

Info log will show you
- recognized text;
- quality of recognition, whith calculated as difference between
  - square difference between original image and noisy one,
  - square difference between recognized image and noisy one.

In file `out.png` you will get a noisy text.

