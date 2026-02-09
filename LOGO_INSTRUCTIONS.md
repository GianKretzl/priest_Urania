# 📸 Como Adicionar a Logo do Sistema

## Passo a Passo

1. **Salve a imagem da logo** que você deseja usar (a imagem com o relógio alado e "NO CRY BABY")

2. **Renomeie o arquivo** para `logo.png`

3. **Copie o arquivo** para o diretório:
   ```
   frontend/public/logo.png
   ```

4. **Pronto!** A logo aparecerá automaticamente em:
   - 📱 Sidebar (menu lateral)
   - 🏠 Página inicial
   - 📄 Outras páginas do sistema

## Especificações Recomendadas

- **Formato:** PNG (com fundo transparente) ou JPG
- **Dimensões:** 800x800 pixels ou maior
- **Peso:** Máximo 500KB para melhor performance

## Fallback

Se a imagem `logo.png` não for encontrada, o sistema usará automaticamente um placeholder SVG.

## Importante

O arquivo deve estar exatamente em:
```
/workspaces/priest_Urania/frontend/public/logo.png
```

Após adicionar o arquivo, recarregue a página no navegador (F5 ou Ctrl+R).
