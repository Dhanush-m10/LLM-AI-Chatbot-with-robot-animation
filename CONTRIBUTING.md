# Contributing to NeuralChat

Thank you for your interest in contributing to NeuralChat! 🎉

## 🚀 How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/neuralchat/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Browser and OS information

### Suggesting Features

1. Check existing [Issues](https://github.com/yourusername/neuralchat/issues) for similar suggestions
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach (optional)

### Pull Requests

1. **Fork** the repository
2. **Clone** your fork:
   ```bash
   git clone https://github.com/yourusername/neuralchat.git
   ```

3. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/AmazingFeature
   ```

4. **Make your changes**:
   - Follow the existing code style
   - Add comments for complex logic
   - Test thoroughly

5. **Commit** your changes:
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```

6. **Push** to your fork:
   ```bash
   git push origin feature/AmazingFeature
   ```

7. **Open a Pull Request** with:
   - Clear title and description
   - Reference any related issues
   - Screenshots/GIFs for UI changes

## 📝 Code Style

### HTML
- Use proper indentation (2 spaces)
- Semantic HTML elements
- Accessible markup (ARIA labels where needed)

### CSS
- Use CSS variables for theming
- Mobile-first approach
- Meaningful class names
- Comments for complex styles

### JavaScript
- ES6+ syntax
- Descriptive variable names
- Comments for complex logic
- Console logs for debugging (remove before PR)

### Example:
```javascript
// Good
async function sendMessage() {
    const message = elements.userInput.value.trim();
    
    if (!message) {
        console.log('Empty message');
        return;
    }
    
    // Send to API...
}

// Avoid
async function sm() {
    const m = document.getElementById('userInput').value;
    if(!m) return;
}
```

## 🧪 Testing

Before submitting a PR:

1. **Test in multiple browsers**:
   - Chrome
   - Firefox
   - Safari
   - Edge

2. **Test responsive design**:
   - Desktop
   - Tablet
   - Mobile

3. **Test with real API**:
   - Valid API key
   - Invalid API key
   - Network errors
   - Long conversations

4. **Check console**:
   - No errors
   - No warnings
   - Meaningful logs

## 🎨 UI/UX Guidelines

- Maintain the retro-futuristic theme
- Use existing color variables
- Ensure accessibility (WCAG 2.1 AA)
- Smooth animations (< 300ms)
- Responsive on all screen sizes

## 🐛 Bug Fix Checklist

- [ ] Bug is reproducible
- [ ] Root cause identified
- [ ] Fix implemented
- [ ] Tested in multiple browsers
- [ ] No new console errors
- [ ] Existing features still work

## ✨ Feature Checklist

- [ ] Feature is well-defined
- [ ] Implementation matches design
- [ ] Tested thoroughly
- [ ] Documentation updated
- [ ] No performance regression
- [ ] Mobile-friendly

## 📚 Documentation

When adding features:

1. Update README.md
2. Add code comments
3. Update SETUP_GUIDE.md if needed
4. Add examples in QUICKSTART.md

## 🎯 Priority Areas

We especially welcome contributions in:

- [ ] Voice input/output
- [ ] Multiple AI model support
- [ ] Chat history export
- [ ] Accessibility improvements
- [ ] Performance optimization
- [ ] Mobile experience
- [ ] Dark/Light theme toggle
- [ ] Internationalization (i18n)

## 💬 Communication

- Be respectful and constructive
- Ask questions if unsure
- Provide context in discussions
- Be patient with reviews

## 🏆 Recognition

Contributors will be:
- Listed in README.md
- Mentioned in release notes
- Given credit in documentation

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## ❓ Questions?

Feel free to:
- Open an issue
- Ask in Pull Request comments
- Reach out to maintainers

---

**Thank you for making NeuralChat better! 🚀**
