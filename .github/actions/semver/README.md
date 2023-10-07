# SemVer docker action



## Inputs

## Outputs

### `next_tag`

...

### `changelog_delta`

...

## Example usage

```yaml
      - name: Semver
        uses: ./.github/actions/semver
        id: semver
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```