
<section class="detail-section">
    <h3>Effort breakdown</h3>
    <ul>
        <li>
            Learning: {{ result.learning_hours }} hours
        </li>
        <li>
            Building: {{ result.build_hours }} hours
        </li>
        <li>
            Testing: {{ result.testing_hours }} hours
        </li>
        <li>
            Deployment: {{ result.deployment_hours }} hours
        </li>
        <li>
            <strong>
                Total: {{ result.required_hours }} hours
            </strong>
        </li>
    </ul>
</section>
</div>
</div>

<div class="scope-box">
    <h3>Recommended execution strategy</h3>
    <p>
        {% if result.status == "Feasible" %}
            Start with the core feature, test it with realistic examples,
            and then improve the interface and deployment.
        {% elif result.status == "Tight" %}
            Prioritise one complete working feature. Reduce optional features
            and reserve time for testing before the deadline.
        {% else %}
            Reduce the scope significantly or extend the deadline.
            Confirm the essential prerequisites before starting the full project.
        {% endif %}
    </p>
    <p style="margin-top: 10px;">
        <strong>Suggested smaller version:</strong>
        {{ result.project.reduced_scope }}
    </p>
</div>
</article>
{% endfor %}
</div>
</section>
