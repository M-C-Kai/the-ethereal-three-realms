.class public final Lpmsj/work/b/a;
.super Ljava/lang/Object;


# static fields
.field public static a:B

.field public static b:B

.field static c:Ljava/util/Vector;

.field public static d:B

.field private static e:La/c/e;

.field private static f:Ljava/util/Vector;

.field private static g:Ljava/util/Vector;

.field private static h:Ljava/util/Vector;


# direct methods
.method static constructor <clinit>()V
    .locals 3

    const/4 v2, 0x2

    const/4 v1, 0x5

    const/4 v0, 0x4

    sput-byte v0, Lpmsj/work/b/a;->a:B

    sput-byte v1, Lpmsj/work/b/a;->b:B

    new-instance v0, La/c/e;

    invoke-direct {v0, v2}, La/c/e;-><init>(I)V

    sput-object v0, Lpmsj/work/b/a;->e:La/c/e;

    new-instance v0, Ljava/util/Vector;

    invoke-direct {v0, v1}, Ljava/util/Vector;-><init>(I)V

    sput-object v0, Lpmsj/work/b/a;->f:Ljava/util/Vector;

    new-instance v0, Ljava/util/Vector;

    invoke-direct {v0, v2}, Ljava/util/Vector;-><init>(I)V

    sput-object v0, Lpmsj/work/b/a;->g:Ljava/util/Vector;

    new-instance v0, Ljava/util/Vector;

    invoke-direct {v0, v1}, Ljava/util/Vector;-><init>(I)V

    sput-object v0, Lpmsj/work/b/a;->h:Ljava/util/Vector;

    new-instance v0, Ljava/util/Vector;

    invoke-direct {v0}, Ljava/util/Vector;-><init>()V

    sput-object v0, Lpmsj/work/b/a;->c:Ljava/util/Vector;

    return-void
.end method

.method public constructor <init>()V
    .locals 0

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static a(B)Lpmsj/work/b/g;
    .locals 4

    sget-object v0, Lpmsj/work/b/a;->h:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v1

    const/4 v0, 0x0

    move v2, v0

    :goto_0
    if-ge v2, v1, :cond_1

    sget-object v0, Lpmsj/work/b/a;->h:Ljava/util/Vector;

    invoke-virtual {v0, v2}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lpmsj/work/b/g;

    invoke-virtual {v0, p0}, Lpmsj/work/b/g;->f(B)Z

    move-result v3

    if-eqz v3, :cond_0

    :goto_1
    return-object v0

    :cond_0
    add-int/lit8 v0, v2, 0x1

    move v2, v0

    goto :goto_0

    :cond_1
    const/4 v0, 0x0

    goto :goto_1
.end method

.method public static a(II)Lpmsj/work/b/j;
    .locals 1

    invoke-static {p1}, Lpmsj/work/b/j;->g(I)Z

    move-result v0

    if-eqz v0, :cond_1

    invoke-static {p1}, Lpmsj/work/b/j;->h(I)Z

    move-result v0

    if-eqz v0, :cond_0

    new-instance v0, Lpmsj/work/b/r;

    invoke-direct {v0, p0, p1}, Lpmsj/work/b/r;-><init>(II)V

    :goto_0
    return-object v0

    :cond_0
    new-instance v0, Lpmsj/work/b/g;

    invoke-direct {v0, p0, p1}, Lpmsj/work/b/g;-><init>(II)V

    goto :goto_0

    :cond_1
    new-instance v0, Lpmsj/work/b/j;

    invoke-direct {v0, p0, p1}, Lpmsj/work/b/j;-><init>(II)V

    goto :goto_0
.end method

.method public static a(ILjava/util/Vector;)Lpmsj/work/b/j;
    .locals 4

    invoke-virtual {p1}, Ljava/util/Vector;->size()I

    move-result v1

    const/4 v0, 0x0

    move v2, v0

    :goto_0
    if-ge v2, v1, :cond_1

    invoke-virtual {p1, v2}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lpmsj/work/b/j;

    iget v3, v0, Lpmsj/work/b/j;->e:I

    if-ne v3, p0, :cond_0

    :goto_1
    return-object v0

    :cond_0
    add-int/lit8 v0, v2, 0x1

    move v2, v0

    goto :goto_0

    :cond_1
    const/4 v0, 0x0

    goto :goto_1
.end method

.method public static a()V
    .locals 1

    sget-object v0, Lpmsj/work/b/a;->f:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->removeAllElements()V

    sget-object v0, Lpmsj/work/b/a;->g:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->removeAllElements()V

    sget-object v0, Lpmsj/work/b/a;->h:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->removeAllElements()V

    sget-object v0, Lpmsj/work/b/a;->c:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->removeAllElements()V

    sget-object v0, Lpmsj/work/b/a;->e:La/c/e;

    invoke-virtual {v0}, La/c/e;->e()V

    return-void
.end method

.method public static a(I)V
    .locals 2

    sget-object v0, Lpmsj/work/b/a;->c:Ljava/util/Vector;

    invoke-static {p0, v0}, Lpmsj/work/b/a;->b(ILjava/util/Vector;)Lpmsj/work/b/j;

    move-result-object v0

    if-eqz v0, :cond_0

    sget-object v1, Lpmsj/work/b/a;->f:Ljava/util/Vector;

    invoke-virtual {v1, v0}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_0
    return-void
.end method

.method public static a(ILjava/lang/String;)V
    .locals 1

    sget-object v0, Lpmsj/work/b/a;->e:La/c/e;

    invoke-virtual {v0, p0, p1}, La/c/e;->a(ILjava/lang/Object;)Ljava/lang/Object;

    return-void
.end method

.method private static a(Ljava/util/Vector;)V
    .locals 8

    const/4 v7, 0x0

    invoke-virtual {p0}, Ljava/util/Vector;->size()I

    move-result v2

    move v3, v7

    :goto_0
    if-ge v3, v2, :cond_2

    move v4, v7

    :goto_1
    sub-int v0, v2, v3

    const/4 v1, 0x1

    sub-int/2addr v0, v1

    if-ge v4, v0, :cond_1

    invoke-virtual {p0, v4}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lpmsj/work/b/j;

    add-int/lit8 v1, v4, 0x1

    invoke-virtual {p0, v1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Lpmsj/work/b/j;

    iget-short v5, v0, Lpmsj/work/b/j;->t:S

    iget-short v6, v1, Lpmsj/work/b/j;->t:S

    if-le v5, v6, :cond_0

    invoke-virtual {p0, v1, v4}, Ljava/util/Vector;->setElementAt(Ljava/lang/Object;I)V

    add-int/lit8 v1, v4, 0x1

    invoke-virtual {p0, v0, v1}, Ljava/util/Vector;->setElementAt(Ljava/lang/Object;I)V

    :cond_0
    add-int/lit8 v0, v4, 0x1

    move v4, v0

    goto :goto_1

    :cond_1
    add-int/lit8 v0, v3, 0x1

    move v3, v0

    goto :goto_0

    :cond_2
    return-void
.end method

.method public static a(Ljava/util/Vector;Ljava/util/Vector;Ljava/util/Vector;Ljava/util/Vector;)V
    .locals 5

    const/4 v4, 0x0

    invoke-virtual {p0}, Ljava/util/Vector;->size()I

    move-result v0

    new-instance v1, Ljava/util/Vector;

    invoke-direct {v1}, Ljava/util/Vector;-><init>()V

    const/4 v2, 0x1

    sub-int/2addr v0, v2

    move v2, v0

    :goto_0
    if-ltz v2, :cond_0

    invoke-virtual {p0, v2}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lpmsj/work/b/j;

    iget-short v3, v0, Lpmsj/work/b/j;->s:S

    sparse-switch v3, :sswitch_data_0

    :goto_1
    add-int/lit8 v0, v2, -0x1

    move v2, v0

    goto :goto_0

    :sswitch_0
    invoke-virtual {p2, v0}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto :goto_1

    :sswitch_1
    invoke-virtual {p1, v0}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto :goto_1

    :sswitch_2
    invoke-virtual {p3, v0}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto :goto_1

    :sswitch_3
    invoke-virtual {v1, v0}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto :goto_1

    :cond_0
    invoke-static {p1}, Lpmsj/work/b/a;->a(Ljava/util/Vector;)V

    invoke-static {p2}, Lpmsj/work/b/a;->b(Ljava/util/Vector;)V

    move v0, v4

    move v1, v4

    :goto_2
    invoke-virtual {p2}, Ljava/util/Vector;->size()I

    move-result v2

    sub-int/2addr v2, v1

    if-ge v0, v2, :cond_4

    invoke-virtual {p2, v0}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, Lpmsj/work/b/g;

    const/16 v2, 0x200

    invoke-virtual {p0, v2}, Lpmsj/work/b/g;->k(I)Z

    move-result v2

    if-eqz v2, :cond_1

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v2

    invoke-virtual {v2}, Lpmsj/work/b/ab;->q()Z

    move-result v2

    if-nez v2, :cond_2

    :cond_1
    const/16 v2, 0x400

    invoke-virtual {p0, v2}, Lpmsj/work/b/g;->k(I)Z

    move-result v2

    if-eqz v2, :cond_3

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v2

    invoke-virtual {v2}, Lpmsj/work/b/ab;->q()Z

    move-result v2

    if-nez v2, :cond_3

    :cond_2
    invoke-virtual {p2, v0}, Ljava/util/Vector;->removeElementAt(I)V

    invoke-virtual {p2, p0}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    add-int/lit8 v1, v1, 0x1

    goto :goto_2

    :cond_3
    add-int/lit8 v0, v0, 0x1

    goto :goto_2

    :cond_4
    return-void

    :sswitch_data_0
    .sparse-switch
        0x64 -> :sswitch_0
        0x96 -> :sswitch_1
        0xa0 -> :sswitch_2
        0xaa -> :sswitch_3
    .end sparse-switch
.end method

.method public static b()Ljava/util/Vector;
    .locals 1

    sget-object v0, Lpmsj/work/b/a;->c:Ljava/util/Vector;

    return-object v0
.end method

.method public static b(I)Lpmsj/work/b/j;
    .locals 1

    sget-object v0, Lpmsj/work/b/a;->f:Ljava/util/Vector;

    invoke-static {p0, v0}, Lpmsj/work/b/a;->a(ILjava/util/Vector;)Lpmsj/work/b/j;

    move-result-object v0

    if-eqz v0, :cond_1

    :cond_0
    :goto_0
    return-object v0

    :cond_1
    sget-object v0, Lpmsj/work/b/a;->g:Ljava/util/Vector;

    invoke-static {p0, v0}, Lpmsj/work/b/a;->a(ILjava/util/Vector;)Lpmsj/work/b/j;

    move-result-object v0

    if-nez v0, :cond_0

    sget-object v0, Lpmsj/work/b/a;->h:Ljava/util/Vector;

    invoke-static {p0, v0}, Lpmsj/work/b/a;->a(ILjava/util/Vector;)Lpmsj/work/b/j;

    move-result-object v0

    goto :goto_0
.end method

.method public static b(ILjava/util/Vector;)Lpmsj/work/b/j;
    .locals 4

    invoke-virtual {p1}, Ljava/util/Vector;->size()I

    move-result v1

    const/4 v0, 0x0

    move v2, v0

    :goto_0
    if-ge v2, v1, :cond_1

    invoke-virtual {p1, v2}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lpmsj/work/b/j;

    iget v3, v0, Lpmsj/work/b/j;->e:I

    if-ne v3, p0, :cond_0

    invoke-virtual {p1, v2}, Ljava/util/Vector;->removeElementAt(I)V

    :goto_1
    return-object v0

    :cond_0
    add-int/lit8 v0, v2, 0x1

    move v2, v0

    goto :goto_0

    :cond_1
    const/4 v0, 0x0

    goto :goto_1
.end method

.method public static b(II)V
    .locals 2

    invoke-static {p0}, Lpmsj/work/b/a;->d(I)Lpmsj/work/b/j;

    move-result-object v0

    if-eqz v0, :cond_0

    iput p1, v0, Lpmsj/work/b/j;->v:I

    sget-object v1, Lpmsj/work/b/a;->c:Ljava/util/Vector;

    invoke-virtual {v1, v0}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_0
    return-void
.end method

.method private static b(Ljava/util/Vector;)V
    .locals 8

    const/4 v7, 0x0

    invoke-virtual {p0}, Ljava/util/Vector;->size()I

    move-result v2

    move v3, v7

    :goto_0
    if-ge v3, v2, :cond_2

    move v4, v7

    :goto_1
    sub-int v0, v2, v3

    const/4 v1, 0x1

    sub-int/2addr v0, v1

    if-ge v4, v0, :cond_1

    invoke-virtual {p0, v4}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lpmsj/work/b/j;

    add-int/lit8 v1, v4, 0x1

    invoke-virtual {p0, v1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Lpmsj/work/b/j;

    iget-byte v5, v0, Lpmsj/work/b/j;->n:B

    iget-byte v6, v1, Lpmsj/work/b/j;->n:B

    if-ge v5, v6, :cond_0

    invoke-virtual {p0, v1, v4}, Ljava/util/Vector;->setElementAt(Ljava/lang/Object;I)V

    add-int/lit8 v1, v4, 0x1

    invoke-virtual {p0, v0, v1}, Ljava/util/Vector;->setElementAt(Ljava/lang/Object;I)V

    :cond_0
    add-int/lit8 v0, v4, 0x1

    move v4, v0

    goto :goto_1

    :cond_1
    add-int/lit8 v0, v3, 0x1

    move v3, v0

    goto :goto_0

    :cond_2
    return-void
.end method

.method public static c()I
    .locals 2

    sget-object v0, Lpmsj/work/b/a;->f:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    sget-object v1, Lpmsj/work/b/a;->c:Ljava/util/Vector;

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v1

    add-int/2addr v0, v1

    return v0
.end method

.method public static c(I)Lpmsj/work/b/j;
    .locals 4

    sget-object v0, Lpmsj/work/b/a;->f:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v1

    const/4 v0, 0x0

    move v2, v0

    :goto_0
    if-ge v2, v1, :cond_1

    sget-object v0, Lpmsj/work/b/a;->f:Ljava/util/Vector;

    invoke-virtual {v0, v2}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lpmsj/work/b/j;

    iget v3, v0, Lpmsj/work/b/j;->f:I

    if-ne v3, p0, :cond_0

    :goto_1
    return-object v0

    :cond_0
    add-int/lit8 v0, v2, 0x1

    move v2, v0

    goto :goto_0

    :cond_1
    const/4 v0, 0x0

    goto :goto_1
.end method

.method public static d(I)Lpmsj/work/b/j;
    .locals 1

    sget-object v0, Lpmsj/work/b/a;->f:Ljava/util/Vector;

    invoke-static {p0, v0}, Lpmsj/work/b/a;->b(ILjava/util/Vector;)Lpmsj/work/b/j;

    move-result-object v0

    if-eqz v0, :cond_1

    :cond_0
    :goto_0
    return-object v0

    :cond_1
    sget-object v0, Lpmsj/work/b/a;->g:Ljava/util/Vector;

    invoke-static {p0, v0}, Lpmsj/work/b/a;->b(ILjava/util/Vector;)Lpmsj/work/b/j;

    move-result-object v0

    if-nez v0, :cond_0

    sget-object v0, Lpmsj/work/b/a;->h:Ljava/util/Vector;

    invoke-static {p0, v0}, Lpmsj/work/b/a;->b(ILjava/util/Vector;)Lpmsj/work/b/j;

    move-result-object v0

    goto :goto_0
.end method

.method public static d()V
    .locals 4

    sget-object v0, Lpmsj/work/b/a;->c:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    const/4 v1, 0x0

    :goto_0
    if-ge v1, v0, :cond_0

    sget-object v2, Lpmsj/work/b/a;->f:Ljava/util/Vector;

    sget-object v3, Lpmsj/work/b/a;->c:Ljava/util/Vector;

    invoke-virtual {v3, v1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v3

    invoke-virtual {v2, v3}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    add-int/lit8 v1, v1, 0x1

    goto :goto_0

    :cond_0
    sget-object v0, Lpmsj/work/b/a;->c:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->removeAllElements()V

    return-void
.end method

.method public static e()Ljava/util/Vector;
    .locals 1

    sget-object v0, Lpmsj/work/b/a;->f:Ljava/util/Vector;

    return-object v0
.end method

.method public static e(I)V
    .locals 1

    sget-object v0, Lpmsj/work/b/a;->e:La/c/e;

    invoke-virtual {v0, p0}, La/c/e;->c(I)Ljava/lang/Object;

    return-void
.end method

.method public static f(I)Ljava/lang/String;
    .locals 1

    sget-object v0, Lpmsj/work/b/a;->e:La/c/e;

    invoke-virtual {v0, p0}, La/c/e;->b(I)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, Ljava/lang/String;

    return-object p0
.end method

.method public static f()Ljava/util/Vector;
    .locals 1

    sget-object v0, Lpmsj/work/b/a;->g:Ljava/util/Vector;

    return-object v0
.end method

.method public static g()Ljava/util/Vector;
    .locals 1

    sget-object v0, Lpmsj/work/b/a;->h:Ljava/util/Vector;

    return-object v0
.end method

.method public static h()I
    .locals 4

    sget-object v0, Lpmsj/work/b/a;->h:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v1

    const/4 v0, 0x0

    move v2, v0

    :goto_0
    if-ge v2, v1, :cond_1

    sget-object v0, Lpmsj/work/b/a;->h:Ljava/util/Vector;

    invoke-virtual {v0, v2}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lpmsj/work/b/g;

    const/16 v3, 0xa

    invoke-virtual {v0, v3}, Lpmsj/work/b/g;->f(B)Z

    move-result v3

    if-eqz v3, :cond_0

    invoke-virtual {v0}, Lpmsj/work/b/g;->h()I

    move-result v0

    :goto_1
    return v0

    :cond_0
    add-int/lit8 v0, v2, 0x1

    move v2, v0

    goto :goto_0

    :cond_1
    const/4 v0, -0x1

    goto :goto_1
.end method
